from Acquisition import aq_inner
from time import time
from zope.component import queryAdapter
from zope.component import queryMultiAdapter

from plone.memoize import view, ram

from Products.Archetypes.atapi import DisplayList
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView

from collective.perseo import perseoMessageFactory as _
from collective.perseo.browser.seo_config import ISEOConfigSchema

from zope.annotation.interfaces import IAnnotations


PERSEO_PREFIX = 'perseo_'
SUFFIX = '_override'
PROP_PREFIX = 'pSEO_'


# Ram cache function, which depends on plone instance and time
def plone_instance_time(method, self, *args, **kwargs):
    return (self.pps.portal(), time() // (60 * 60))


class PerSEOGenericContext(BrowserView):
    """ Calculate html header meta tags on context.
    """

    def __init__(self, *args, **kwargs):
        super(PerSEOGenericContext, self).__init__(*args, **kwargs)
        self.pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        self.pcs = queryMultiAdapter((self.context, self.request), name="plone_context_state")
        self.gseo = queryAdapter(self.pps.portal(), ISEOConfigSchema)
        self._perseo_metatags = self._getPerSEOMetaTags()

    def __getitem__(self, key):
        return self._perseo_metatags.get(key, '')

    @view.memoize
    def _getPerSEOMetaTags(self):
        perseo_metatags = {
            "googleWebmasterTools": self.seo_globalGoogleWebmasterTools(),
            "yahooSiteExplorer": self.seo_globalYahooSiteExplorer(),
            "bingWebmasterTools": self.seo_globalBingWebmasterTools(),
            "perseo_title": self.perseo_title(),
            "has_perseo_title": self.has_prop('pSEO_title'),
            "has_perseo_title_config": self.has_perseo_title_config(),
            "perseo_description": self.perseo_description(),
            "has_perseo_description": self.has_prop('pSEO_description'),
            "perseo_keywords": self.perseo_keywords(),
            "has_perseo_keywords": self.has_prop('pSEO_keywords'),
            "perseo_robots_follow": self.perseo_robots_follow(),
            "perseo_robots_index": self.perseo_robots_index(),
            "perseo_robots_advanced": self.perseo_robots_advanced(),
            "has_perseo_robots_advanced": self.has_prop('pSEO_robots_advanced'),
            "perseo_canonical": self.perseo_canonical(),
            "has_perseo_canonical": self.has_prop('pSEO_canonical'),
            "perseo_included_in_sitemapxml": self.perseo_included_in_sitemapxml(),
            "perseo_priority_sitemapxml": self.perseo_priority_sitemapxml(),
            "perseo_itemtype": self.perseo_itemtype(),
            "has_perseo_itemtype": self.has_prop('pSEO_itemtype'),
            "has_perseo_robots_follow": self.has_prop('pSEO_robots_follow'),
            "has_perseo_robots_index": self.has_prop('pSEO_robots_index'),
            "has_perseo_included_in_sitemapxml": self.has_prop('pSEO_included_in_sitemapxml'),
            }
        return perseo_metatags

    def has_prop(self, property):
        try:
            return property in IAnnotations(self.context)
        except:
            return None

    def getYesNoOptions(self):
        """Get a sample vocabulary
        """
        return DisplayList((("yes", _(u"Yes"),),
                            ("no", _(u"No"),),
                            ))

    def getRobotsAdvanced(self):
        """Get a sample vocabulary for Robots Advanced options
        """
        return DisplayList((("", _(u"None"),),
                            ("noodp", _(u"NO ODP"),),
                            ("noydir", _(u"NO YDIR"),),
                            ("noarchive", _(u"No Archive"),),
                            ("nosnippet", _(u"No Snippet"),),
                            ))

    def getPerSEOProperty(self, property_name, accessor='', default=None):
        """ Get value from seo property by property name.
        """
        context = aq_inner(self.context)

        try:
            annotations = IAnnotations(context)
            if property_name in annotations:
                return annotations.get(property_name, default)
        except:  # BBB this cannot be like that!!!!!
            return default

        if accessor:
            method = getattr(context, accessor, default)
            if not callable(method):
                return default

            # Catch AttributeErrors raised by some AT applications
            try:
                value = method()
            except AttributeError:
                value = default

            return value

        return default

    @property
    def unified_template_id(self):
        # I take template_id as it is done in ploneview
        # if all goes OK for ploneview it is fine in my general view
        template_id = None
        if 'PUBLISHED' in self.request:
            if getattr(self.request['PUBLISHED'], 'getId', None):
                # template inside skins   
                template_id = self.request['PUBLISHED'].getId()
            if getattr(self.request['PUBLISHED'], __name__, None):
                # template inside browser view
                template_id = self.request['PUBLISHED'].__name__
        if template_id:
            if template_id == 'search' or template_id == 'search_form':
                return 'searchpage'
            elif template_id == 'author':
                return 'authorpage'
            elif template_id == 'sitemap':
                return 'sitemappage'
            elif template_id == 'accessibility-info':
                return 'accessibilitypage'
            elif template_id == 'contact-info':
                return 'contactpage'
            elif template_id in ('login','logout','logged','registered'):
                return 'loginregistrationpage'
            elif template_id == 'plone_control_panel':
                return 'administrationpage'
            else:
                return 'homepage'
        else:
            try:
                self.context.restrictedTraverse(self.request.PATH_INFO)
                return 'homepage'
            except:
                return 'notfoundpage'

    @ram.cache(plone_instance_time)
    def seo_globalGoogleWebmasterTools(self):
        """ Returned Google Webmaster Tools from Plone SEO Configuration Control Panel Tool
        """
        result = ''
        if self.gseo:
            result = self.gseo.googleWebmasterTools
        return result
    
    @ram.cache(plone_instance_time)
    def seo_globalYahooSiteExplorer( self ):
        """ Returned Yahoo Site Explorer from Plone SEO Configuration Control Panel Tool
        """
        result = ''
        if self.gseo:
            result = self.gseo.yahooSiteExplorer
        return result
    
    @ram.cache(plone_instance_time)
    def seo_globalBingWebmasterTools( self ):
        """ Returned Bing Webmaster Tools from Plone SEO Configuration Control Panel Tool
        """
        result = ''
        if self.gseo:
            result = self.gseo.bingWebmasterTools
        return result
    
    def get_gseo_field( self, field ):
        """ Returned field from Plone SEO Configuration Control Panel Tool
        """
        result = None
        if self.gseo:
            result = getattr(self.gseo, field, None)
        return result
    
    def perseo_variables(self, value):
        if value:
            if isinstance(value, (list, tuple)):
                new_value = []
                for x in value:
                    new_value.append(safe_unicode(x.replace('%%title%%',self.pcs.context.Title()).\
                                                    replace('%%tag%%',' '.join(self.pcs.context.Subject()))))
                return new_value
            return safe_unicode(value.replace('%%title%%',self.pcs.context.Title()).\
                                    replace('%%tag%%',' '.join(self.pcs.context.Subject())))
        return value


class PerseoTabAvailable(BrowserView):
    """"""

    def checkPerseoTabAvailable(self):
        """ Checks visibility of SEO tab for context
        """
        return True

