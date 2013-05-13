from Acquisition import aq_inner
from cgi import escape

from zope.component import getMultiAdapter, queryAdapter, queryMultiAdapter
from plone.app.layout.viewlets.common import ViewletBase
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode, getSiteEncoding

from collective.perseo.browser.seo_config import ISEOConfigSchema
from collective.perseo.utils import SortedDict


# mapping {meta_name:accessor} of all meta tags
METATAGS = {"google-site-verification":"googleWebmasterTools",
            "msvalidate.01":"bingWebmasterTools",
            "description":"perseo_description",
            "keywords":"perseo_keywords",
            "robots":"perseo_robots"}

METATAGS_ORDER = ["google-site-verification",
                  "msvalidate.01",
                  "description",
                  "keywords",
                  "robots"]


class PerSEOMetaTagsViewlet( ViewletBase ):
    """Inserts meta tags in html head of pages"""

    def render(self):
        TEMPLATE = '<meta name="%s" content="%s"/>'
        enc = getSiteEncoding(self.context)
        sfuncd = lambda x, enc=enc:escape(safe_unicode(x, enc))

        meta_tags = []

        for k,v in self.listMetaTags().items():
            if isinstance(v, (list, tuple)):
                for x in v:
                    meta_tags.append((k,x))
            else:
                meta_tags.append((k,v))

        return u'\n'.join([TEMPLATE % tuple(map(sfuncd, (k,v))) \
                           for k,v in meta_tags])

    def listMetaTags(self):
        """Calculate list metatags"""

        result = SortedDict()
        #pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        #seo_global = queryAdapter(pps.portal(), ISEOConfigSchema)
        seo_context = queryMultiAdapter((self.context, self.request), name='perseo-context')

        for key in METATAGS_ORDER:
            accessor = METATAGS[key]
            if seo_context._perseo_metatags.has_key(accessor):
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

            if isinstance(value, (list, tuple)): #and not key == "robots":
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
        self.pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        self.gseo = queryAdapter(self.pps.portal(), ISEOConfigSchema)
        self.pm = getToolByName(self.context, 'portal_membership')

    def render(self):
        result = ""
        opts = {'canonical': self.perseo_context['perseo_canonical'],
                'alternate': self.perseo_context['alternate_i18n']}
        if self.gseo and self.gseo.google_publisher:
            opts['google_publisher'] = self.gseo.google_publisher

        author = self.pm.getMemberById(self.context.Creator())
        if author and author.getProperty('google_author'):
            opts['google_author'] = author.getProperty('google_author')

        if opts['canonical']:
            result += """<link rel="canonical" href="%(canonical)s" />\n""" % opts
        if opts['alternate']:
            for lang, translation in opts['alternate'].items():
                result += """<link rel="alternate" hreflang="%s" href="%s" />\n""" % (lang, translation.absolute_url())
        if opts.get('google_publisher'):
            result += """<link href="%(google_publisher)s" rel="publisher" />\n""" % opts
        if opts.get('google_author'):
            result += """<link href="%(google_author)s" rel="author" />\n""" % opts
        return result


class TrackingCodeViewlet( ViewletBase ):
    """ Simple viewlet for script rendering.
    """
    def update(self):
        self.pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        self.gseo = queryAdapter(self.pps.portal(), ISEOConfigSchema)

    def getTrackingCode( self ):
        return ''

    def render( self ):
        return safe_unicode("""%s""" % self.getTrackingCode())


class TrackingCodeHeaderViewlet( TrackingCodeViewlet ):
    """ Simple viewlet for script rendering in the <head>.
    """
    def getTrackingCode( self ):
        if self.gseo:
            return self.gseo.tracking_code_header
        return ''


class TrackingCodeFooterViewlet( TrackingCodeViewlet ):
    """ Simple viewlet for script rendering in the portal footer.
    """
    def getTrackingCode( self ):
        if self.gseo:
            return self.gseo.tracking_code_footer
        return ''
