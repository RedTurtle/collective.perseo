from Acquisition import aq_inner
from cgi import escape

#from zope.component import queryAdapter
from zope.component import getMultiAdapter, queryAdapter, queryMultiAdapter
from plone.app.layout.viewlets.common import ViewletBase

from Products.CMFPlone.utils import safe_unicode, getSiteEncoding

from collective.perseo.browser.seo_config import ISEOConfigSchema
from collective.perseo.util import SortedDict

# mapping {meta_name:accessor} of all meta tags
METATAGS = {"google-site-verification": "googleWebmasterTools",
            "y_key": "yahooSiteExplorer",
            "msvalidate.01": "bingWebmasterTools",
            "description": "perseo_description",
            "keywords": "perseo_keywords",
            "robots": "perseo_robots"}

METATAGS_ORDER = ["google-site-verification",
                  "y_key",
                  "msvalidate.01",
                  "description",
                  "keywords",
                  "robots"]


class PerSEOMetaTagsViewlet(ViewletBase):
    """Inserts meta tags in html head of pages"""

    def render(self):
        TEMPLATE = '<meta name="%s" content="%s"/>'
        enc = getSiteEncoding(self.context)
        sfuncd = lambda x, enc=enc: escape(safe_unicode(x, enc))
        meta_tags = []

        for k, v in self.listMetaTags().items():
            if isinstance(v, (list, tuple)):
                for x in v:
                    meta_tags.append((k, x))
            else:
                meta_tags.append((k, v))

        return u'\n'.join([TEMPLATE % tuple(map(sfuncd, (k, v))) \
                           for k, v in meta_tags])

    def listMetaTags(self):
        """Calculate list metatags"""

        result = SortedDict()
        seo_context = queryMultiAdapter((self.context, self.request), name='perseo-context')

        for key in METATAGS_ORDER:
            accessor = METATAGS[key]
            if accessor in seo_context._perseo_metatags:
                value = seo_context._perseo_metatags.get(accessor, None)
            else:
                method = getattr(seo_context, accessor, None)
                if method is None:
                    method = getattr(aq_inner(self.context).aq_explicit, accessor, None)

                if not callable(method):
                    continue

                # Catch AttributeErrors raised by some AT applications
                try:
                    value = method()
                except AttributeError:
                    value = None

            if not value:
                # No data
                continue

            if isinstance(value, (list, tuple)):  # and not key == "robots":
                # convert a list to a string
                value = ', '.join(value)

            result[key] = value

        return result


class PerSEOTitleTagViewlet(ViewletBase):
    """ Viewlet for custom title tag rendering.
    """

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
        self.perseo_context = getMultiAdapter((self.context, self.request),
                                             name=u'perseo-context')

    def std_title(self):
        page_title = safe_unicode(self.context_state.object_title())
        portal_title = safe_unicode(self.portal_state.portal_title())
        if page_title == portal_title:
            return u"<title>%s</title>" % (escape(portal_title))
        else:
            return u"<title>%s &mdash; %s</title>" % (
                escape(safe_unicode(page_title)),
                escape(safe_unicode(portal_title)))

    def render(self):
        if not self.perseo_context['has_perseo_title'] and not self.perseo_context['has_perseo_title_config']:
            return self.std_title()
        else:
            perseo_title = u"<title>%s</title>" % escape(safe_unicode(
                self.perseo_context["perseo_title"]))
            return perseo_title


class PerSEOCanonicalUrlViewlet(ViewletBase):
    """ Simple viewlet for canonical url link rendering.
    """
    def update(self):
        self.perseo_context = getMultiAdapter((self.context, self.request),
                                             name=u'perseo-context')

    def render(self):
        if self.perseo_context['perseo_canonical']:
            return """<link rel="canonical" href="%s" />""" % self.perseo_context['perseo_canonical']
        return ""


class TrackingCodeViewlet(ViewletBase):
    """ Simple viewlet for script rendering.
    """
    def update(self):
        self.pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        self.gseo = queryAdapter(self.pps.portal(), ISEOConfigSchema)

    def getTrackingCode(self):
        return ''

    def render(self):
        return safe_unicode("""%s""" % self.getTrackingCode())


class TrackingCodeHeaderViewlet(TrackingCodeViewlet):
    """ Simple viewlet for script rendering in the <head>.
    """

    def getTrackingCode(self):
        if self.gseo:
            return self.gseo.tracking_code_header
        return ''


class TrackingCodeFooterViewlet(TrackingCodeViewlet):
    """ Simple viewlet for script rendering in the portal footer.
    """

    def getTrackingCode(self):
        if self.gseo:
            return self.gseo.tracking_code_footer
        return ''


class TwitterCardsViewlet(ViewletBase):
    """ Simple viewlet for twitter cards.
    """
    def update(self):
        self.pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        self.global_perseo = queryAdapter(self.pps.portal(), ISEOConfigSchema)
        self.perseo_context = getMultiAdapter((self.context, self.request), name=u'perseo-context')
        self.context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
        mtool = self.context.portal_membership

        creator = mtool.getMemberById(self.context.Creator())
        self.twitter_creator = creator and creator.getProperty('twitter_id','') or 'plone'
        self.twitter_site = self.global_perseo.twitter_site_id
        self.twitter_url = self.perseo_context.perseo_canonical() or self.context.absolute_url()
        self.twitter_card = 'summary'  # BBB: to be finished
        self.twitter_title = self.perseo_context.perseo_title() or self.context_state.object_title()
        self.twitter_description = self.perseo_context.perseo_description()
        self.twitter_image = self.perseo_context.perseo_image()

    def render(self):
        return safe_unicode("""<meta name="twitter:card" content="%(card)s">
        <meta name="twitter:site" content="@%(site)s">
        <meta name="twitter:creator" content="@%(creator)s">
        <meta name="twitter:url" content="%(url)s">
        <meta name="twitter:title" content="%(title)s">
        <meta name="twitter:description" content="%(description)s">
        <meta name="twitter:image" content="%(image)s">
        """ % {'card': self.twitter_card,
               'site': self.twitter_site,
               'creator': self.twitter_creator,
               'url': self.twitter_url,
               'title': self.twitter_title,
               'description': self.twitter_description,
               'image': self.twitter_image})

