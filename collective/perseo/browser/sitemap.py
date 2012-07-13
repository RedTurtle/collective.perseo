from plone.app.layout.sitemap.sitemap import SiteMapView
from zope.component import queryAdapter
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.perseo.browser.seo_config import ISEOConfigSchema


class PerSEOSiteMapView (SiteMapView):
    """Creates the sitemap as explained in the specifications.

    http://www.sitemaps.org/protocol.php
    """
    index = ViewPageTemplateFile('sitemap.xml')

    def __init__(self, context, request):
        super(PerSEOSiteMapView, self).__init__(context, request)
        self.gseo = queryAdapter(self.context, ISEOConfigSchema)

    def template(self):
        " manual unicode encode "
        xml = self.index()
        xml = xml.encode('utf8','ignore')
        return xml

    def get_gseo_field( self, field, default=None):
        """ Returned field from Plone SEO Configuration Control Panel Tool
        """
        if self.gseo:
            return getattr(self.gseo, field, default)
        return default

    def perseo_included_types(self):
        return self.get_gseo_field('not_included_types',default=())

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
        included_types = self.perseo_included_types()
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

