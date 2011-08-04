from collective.perseo.browser.seo_config import ISEOConfigSchema
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations
from zope.component import queryAdapter
import urllib2

def get_gseo(object):
    """ Returned the Adapter for Plone SEO Configuration Control Panel Tool
    """
    portal = getToolByName(object, 'portal_url').getPortalObject()
    return queryAdapter(portal, ISEOConfigSchema)

def get_gseo_field( gseo, field, default=None):
    """ Returned field from Plone SEO Configuration Control Panel Tool
    """
    if gseo:
        return getattr(gseo, field, default)
    return default

def perseo_included_types(object):
    """ Returned the included types in sitemap.xml from Plone SEO Configuration Control Panel Tool
    """
    return get_gseo_field(get_gseo(object),'not_included_types',default=())

def get_included_in_sitemapxml(object):
    """ Returned the value of the pSEO_included_in_sitemapxml annotation attribute of the object
    """
    try:
        annotations = IAnnotations(object)
        if annotations.has_key('pSEO_included_in_sitemapxml'):
            return annotations.get('pSEO_included_in_sitemapxml', None)
    except:
        return None
    return None

def include_in_sitemapxml(object):
    """ Returned True if the object is included in sitemap.xml
    """
    included_types = perseo_included_types(object)
    in_sitemapxml = get_included_in_sitemapxml(object)
    if in_sitemapxml != None:
        return in_sitemapxml
    else:
        return object.portal_type in included_types
    
def url_open(url):
    """ Perform the url open
    """
    try:
        urllib2.urlopen(url)
    except Exception:
        pass

def Pinging(object, event):
    gseo = get_gseo(object)
    
    ping_google = get_gseo_field(gseo,'ping_google',default=False)
    
    ping_yahoo = get_gseo_field(gseo,'ping_yahoo',default=False)
    
    ping_bing = get_gseo_field(gseo,'ping_bing',default=False)
    
    ping_ask = get_gseo_field(gseo,'ping_ask',default=False)
    
    if (ping_google or ping_yahoo or ping_bing or ping_ask) and include_in_sitemapxml(object):
        portal_url = getToolByName(object, 'portal_url')()
        if ping_google:
            url_open("http://submissions.ask.com/ping?sitemap=%s/sitemap.xml.gz" % portal_url)
        if ping_yahoo:
            url_open("http://www.google.com/webmasters/sitemaps/ping?sitemap=%s/sitemap.xml.gz" % portal_url)
        if ping_bing:
            url_open("http://search.yahooapis.com/SiteExplorerService/V1/ping?sitemap=%s/sitemap.xml.gz" % portal_url)
        if ping_ask:
            url_open("http://www.bing.com/webmaster/ping.aspx?siteMap=%s/sitemap.xml.gz" % portal_url)
