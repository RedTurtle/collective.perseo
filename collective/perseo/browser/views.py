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

    def __getitem__(self, key):
        return self._perseo_metatags.get(key, '')
    
    @view.memoize
    def _getPerSEOMetaTags(self):
        perseo_metatags = {
            "googleWebmasterTools": self.seo_globalGoogleWebmasterTools(),
            "yahooSiteExplorer": self.seo_globalYahooSiteExplorer(),
            "bingWebmasterTools":self.seo_globalBingWebmasterTools(),
            "perseo_title":self.perseo_title(),
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
    
    def get_gseo_field( self, field ):
        """ Returned field from Plone SEO Configuration Control Panel Tool
        """
        result = None
        if self.gseo:
            result = getattr(self.gseo, field, None)
        return result
    
    def perseo_title( self ):
        return None

class PerSEOContextPloneSiteRoot(PerSEOContext):
    """ Calculate html header meta tags on context. Context == PloneSiteRoot
    """
    
    def perseo_what_page(self):
        # I take template_id as is done in ploneview
        # if all goes well for ploneview is fine in my general view
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
            else:
                return 'homepage'
        else:
            return 'homepage'

    def perseo_title( self ):
        page = self.perseo_what_page()
        return self.get_gseo_field('%s_title' % page)
            
class PerSEOContextATDocument(PerSEOContext):
    """ Calculate html header meta tags on context. Context == ATDocument
    """
    def perseo_title( self ):
        context = self.pcs.context
        parent = self.pcs.parent()
        
        if parent == self.pps.portal() and parent.getDefaultPage() == context.id:
            # this document is the home page
            return self.get_gseo_field('homepage_title')
        else:
            return self.get_gseo_field('singlepage_title')
