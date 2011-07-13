from time import time
from zope.component import queryAdapter
from zope.component import queryMultiAdapter

from plone.memoize import view, ram

from Products.Five.browser import BrowserView

from collective.perseo.browser.seo_config import ISEOConfigSchema

# Ram cache function, which depends on plone instance and time
def plone_instance_time(method, self, *args, **kwargs):
    return (self.pps.portal(), time() // (60 * 60))

class PerSEOContext(BrowserView):
    """ Calculate html header meta tags on context.
    """

    def __init__(self, *args, **kwargs):
        super(PerSEOContext, self).__init__(*args, **kwargs)
        self.pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        self.pcs = queryMultiAdapter((self.context, self.request), name="plone_context_state")
        self.gseo = queryAdapter(self.pps.portal(), ISEOConfigSchema)
        self._perseo_metatags = self._getPerSEOMetaTags()

    @view.memoize
    def _getPerSEOMetaTags(self):
        perseo_metatags = {
            "googleWebmasterTools": self.seo_globalGoogleWebmasterTools(),
            "yahooSiteExplorer": self.seo_globalYahooSiteExplorer(),
            "bingWebmasterTools":self.seo_globalBingWebmasterTools(),
            }
        return perseo_metatags
    
    @ram.cache(plone_instance_time)
    def seo_globalGoogleWebmasterTools( self ):
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