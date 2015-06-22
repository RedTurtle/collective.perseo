from cgi import escape

from zope.component import getMultiAdapter, queryMultiAdapter
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from plone.app.layout.viewlets.common import ViewletBase
from plone.app.layout.navigation.interfaces import INavigationRoot
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import (safe_unicode,
                                     getSiteEncoding,
                                     safe_hasattr)

from collective.perseo.interfaces import ISEOControlpanel
from collective.perseo.interfaces.settings import ISEOSettings

try:
    from Products.LinguaPlone.browser.contentlinkviewlet import MultilingualContentViewlet as BaseMultilingualContentViewlet
except:
    BaseMultilingualContentViewlet = None


#        <meta name/property=""                    content=""/>
METATAGS = (({"name": "google-site-verification"}, "googleWebmasterTools"),
            ({"name": "msvalidate.01"}, "bingWebmasterTools"),
            ({"name": "description"}, "description"),
            ({"name": "keywords"}, "keywords"),
            ({"name": "robots"}, "robots"),
            ({"name": "twitter:card"}, "twitter_card"),
            ({"name": "twitter:site"}, "twitter_site"),
            ({"name": "twitter:creator"}, "twitter_creator"),
            ({"name": "twitter:image"}, "twitter_image"),
            ({"name": "twitter:description"}, "twitter_description"),
            ({"name": "twitter:title"}, "twitter_title"),
            ({"property": "fb:admins"}, "facebook_admins"),
            ({"property": "og:site_name"}, "og_site_name"),
            ({"property": "og:locale"}, "og_locale"),
            ({"property": "og:type"}, "og_type"),
            ({"property": "og:title"}, "og_title"),
            ({"property": "og:description"}, "og_description"),
            ({"property": "og:url"}, "og_url"),
            ({"property": "og:image"}, "og_image"),
            )


class HrefLangViewlet(ViewletBase):
    """Inserts href lang in html head of pages"""

    # MARKER_CUR = """<link rel='alternate' hreflang='%s' />"""
    MARKER_CUR = """<link rel='alternate' hreflang='%s' href='%s' />"""
    MARKER_TAR = """<link rel='alternate' hreflang='%s' href='%s' />"""
    MARKER_DEF = """<link rel="alternate" href="%s" hreflang="x-default" />"""

    def is_navigation_root(self, obj):
        if INavigationRoot.providedBy(obj):
            return True
        return False

    def render(self):
        """
        for 'translations' variable we have:
        {'en': [<ATDocument at /site/en/front-page>, 'published'],
         'es': [<ATDocument at /site/es/front-page>, 'published'],
         'it': [<ATDocument at /site/it/front-page>, 'published']}
        """
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISEOControlpanel)
        xdef = getattr(settings, 'activate_x_default', False)
        hreflang = getattr(settings, 'activate_hreflang', False)
        link_tag = []

        if not hreflang:
            return u''

        pps = getMultiAdapter((self.context, self.context.REQUEST), name="plone_portal_state")
        pcs = getMultiAdapter((self.context, self.context.REQUEST), name="plone_context_state")
        portal_url = pps.portal_url()
        canonical = pcs.canonical_object()
        pcs.context = canonical

        if xdef and not pcs.is_portal_root() and self.is_navigation_root(canonical):
            link_tag.append(self.MARKER_DEF % portal_url)

        pcs = getMultiAdapter((self.context, self.context.REQUEST), name="plone_context_state")

        if not safe_hasattr(self.context, 'getTranslations'):
            return u'\n'.join(link_tag)

        translations = self.context.getTranslations()
        for translation in translations:
            #if translation == current_lang:
            #    link_tag.append(self.MARKER_CUR % translation)
            #else:
            obj = translations[translation][0]
            pcs.context = obj
            canonical = pcs.canonical_object()
            # be sure that people can see the object
            if 'Anonymous' in obj.__roles__:
                link_tag.append(self.MARKER_TAR % (translation, canonical.absolute_url()))
        return u'\n'.join(link_tag)


class PerSEOMetaTagsViewlet(ViewletBase):
    """Inserts meta tags in html head of pages"""

    def render(self):
        seo = ISEOSettings(self.context, None)
        if not seo:
            return ''
        TEMPLATE = '<meta %(key)s content="%(content)s"/>'
        enc = getSiteEncoding(self.context)
        meta_tags = []

        for seodict, name in METATAGS:
            content = getattr(seo, name, None)
            if not content:
                continue
            if isinstance(content, list) or isinstance(content, tuple):
                content = ', '.join(content).strip().strip(',')

            # each metatag can have more then one name/property
            for k, v in seodict.items():
                opts = {'key': '%s="%s"' % (k, v),  # i.e. name="twitter:card"
                        'content': escape(safe_unicode(content, enc))}
                meta_tags.append(TEMPLATE % opts)
        return u'\n'.join(meta_tags)


class PerSEOTitleTagViewlet(ViewletBase):
    """ Viewlet for custom title tag rendering.
    """

    def update(self):
        self.portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')

    def std_title(self):
        page_title = safe_unicode(self.context_state.object_title())
        portal_title = safe_unicode(self.portal_state.navigation_root_title())
        if page_title == portal_title:
            return u"<title>%s</title>" % (escape(portal_title))
        else:
            return u"<title>%s &mdash; %s</title>" % (
                escape(safe_unicode(page_title)),
                escape(safe_unicode(portal_title)))

    def render(self):
        seo = ISEOSettings(self.context, None)
        page = seo.find_context()
        if seo and (seo.title_override or
                    getattr(seo.settings, '%s_title' % page, None)) \
                and seo.title:
            perseo_title = u"<title>%s</title>" % escape(safe_unicode(
                seo.title))
            return perseo_title
        return self.std_title()


class PerSEOCanonicalUrlViewlet(ViewletBase):
    """ Simple viewlet for canonical url link rendering.
    """
    def update(self):
        self.pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        self.pm = getToolByName(self.context, 'portal_membership')
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISEOControlpanel)

    def render(self):
        result = ""
        seo = ISEOSettings(self.context, None)
        if not seo:
            return result
        opts = {'canonical': seo.canonical_override and seo.canonical,
                'alternate': seo.alternate_i18n}
        if self.settings.google_publisher:
            opts['google_publisher'] = self.settings.google_publisher

        author = self.pm.getMemberById(self.context.Creator())
        if author and author.getProperty('google_author'):
            opts['google_author'] = author.getProperty('google_author')

        if opts['canonical']:
            result += """<link rel="canonical" href="%(canonical)s" />\n""" % opts

        if opts.get('google_publisher'):
            result += """<link href="%(google_publisher)s" rel="publisher" />\n""" % opts
        if opts.get('google_author'):
            result += """<link href="%(google_author)s" rel="author" />\n""" % opts
        return result


class TrackingCodeViewlet(ViewletBase):
    """ Simple viewlet for script rendering.
    """
    def update(self):
        self.pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISEOControlpanel)

    def getTrackingCode(self):
        return ''

    def render(self):
        return safe_unicode("""%s""" % self.getTrackingCode())


class TrackingCodeHeaderViewlet(TrackingCodeViewlet):
    """ Simple viewlet for script rendering in the <head>.
    """
    def getTrackingCode(self):
        return self.settings.tracking_code_header or ''


class TrackingCodeFooterViewlet(TrackingCodeViewlet):
    """ Simple viewlet for script rendering in the portal footer.
    """
    def getTrackingCode(self):
        return self.settings.tracking_code_footer or ''


class MultilingualContentViewlet(BaseMultilingualContentViewlet):

    def update(self):
        return None

    def render(self):
        return ''
