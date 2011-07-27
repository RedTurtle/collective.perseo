from plone.app.layout.sitemap.sitemap import SiteMapView
from Products.CMFCore.utils import getToolByName

from zope.component import queryAdapter

from collective.perseo.browser.seo_config import ISEOConfigSchema

class PerSEOSiteMapView (SiteMapView):
    """Creates the sitemap as explained in the specifications.

    http://www.sitemaps.org/protocol.php
    """
    def __init__(self, context, request):
        super(PerSEOSiteMapView, self).__init__(context, request)
        self.gseo = queryAdapter(self.context, ISEOConfigSchema)
        
    def get_gseo_field( self, field, default=None):
        """ Returned field from Plone SEO Configuration Control Panel Tool
        """
        if self.gseo:
            return getattr(self.gseo, field, default)
        return default
        
    def perseo_included_types(self):
        return self.get_gseo_field('not_included_types',default=())
        
    def objects(self):
        """Returns the data to create the sitemap."""
        
        catalog = getToolByName(self.context, 'portal_catalog')
        
        for item in catalog.searchResults({'Language': 'all'}):
            
            included_types = self.perseo_included_types()
            if item.getIncludedInSitemapxml != None:
                include = item.getIncludedInSitemapxml
            else:
                include = item.portal_type in included_types
            
            if include:
                if item.getPrioritySitemapxml:
                    yield {
                        'loc': item.getURL(),
                        'lastmod': item.modified.ISO8601(),
                        #'changefreq': 'always', # hourly/daily/weekly/monthly/yearly/never
                        'priority': item.getPrioritySitemapxml,
                    }
                else:
                    yield {
                        'loc': item.getURL(),
                        'lastmod': item.modified.ISO8601(),
                        #'changefreq': 'always', # hourly/daily/weekly/monthly/yearly/never
                        #'priority': 0.5, # 0.0 to 1.0
                    }
