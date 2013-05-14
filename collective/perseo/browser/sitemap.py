from plone.app.layout.sitemap.sitemap import SiteMapView
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.perseo.interfaces import ISEOControlpanel


class PerSEOSiteMapView (SiteMapView):
    """Creates the sitemap as explained in the specifications.

    http://www.sitemaps.org/protocol.php
    """
    index = ViewPageTemplateFile('sitemap.xml')

    def __init__(self, context, request):
        super(PerSEOSiteMapView, self).__init__(context, request)
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISEOControlpanel)

    def template(self):
        " manual unicode encode "
        xml = self.index()
        xml = xml.encode('utf8','ignore')
        return xml

    def add_image(self, url, caption=None, title=None):
        image = {'loc': url}
        if caption:
            image.update({'caption': caption.decode('utf8')})
        if title:
            image.update({'title': title.decode('utf8')})
        return image

    def objects(self):
        """Returns the data to create the sitemap."""

        catalog = getToolByName(self.context, 'portal_catalog')
        included_types = self.settings.not_included_types
        image_types = ('Image',)

        for item in catalog.searchResults({'Language': 'all'}):

            if item.getIncludedInSitemapxml != None:
                include = item.getIncludedInSitemapxml
            else:
                include = item.portal_type in included_types

            if include:
                if item.getPrioritySitemapxml:
                    row = {
                        'loc': item.getURL(),
                        'lastmod': item.modified.ISO8601(),
                        #'changefreq': 'always', # hourly/daily/weekly/monthly/yearly/never
                        'priority': item.getPrioritySitemapxml,
                    }
                else:
                    row = {
                        'loc': item.getURL(),
                        'lastmod': item.modified.ISO8601(),
                        #'changefreq': 'always', # hourly/daily/weekly/monthly/yearly/never
                        #'priority': 0.5, # 0.0 to 1.0
                    }
                row['images'] = []
                if hasattr(item, 'hasContentLeadImage') and item.hasContentLeadImage:
                    url = '%s/leadImage' % item.getURL()
                    row['images'].append(self.add_image(url, item.Description, item.Title))

                if item.portal_type in image_types:
                    url = '%s' % item.getURL()
                    row['images'].append(self.add_image(url, item.Description, item.Title))

                yield row

