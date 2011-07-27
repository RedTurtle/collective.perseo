from plone.app.layout.sitemap.sitemap import SiteMapView
from Products.CMFCore.utils import getToolByName

class PerSEOSiteMapView (SiteMapView):
    """Creates the sitemap as explained in the specifications.

    http://www.sitemaps.org/protocol.php
    """
    def __init__(self, context, request):
        super(PerSEOSiteMapView, self).__init__(context, request)
        
    def objects(self):
        """Returns the data to create the sitemap."""
        
        catalog = getToolByName(self.context, 'portal_catalog')
        
        for item in catalog.searchResults({'Language': 'all'}):
            if item.getIncludedInSitemapxml:
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
