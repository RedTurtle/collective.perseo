#from zope.interface import Interface
from Products.Archetypes.interfaces.base import IBaseContent
from plone.indexer.decorator import indexer

from zope.app.component.hooks import getSite
from zope.component import queryAdapter

from collective.perseo.browser.seo_config import ISEOConfigSchema

def perseo_included_types(object):
    portal = getSite()
    gseo = queryAdapter(portal, ISEOConfigSchema)
    if gseo:
        return getattr(gseo, 'not_included_types', ())
    return ()

@indexer(IBaseContent)
def get_included_in_sitemapxml(object, **kw):
    included_types = perseo_included_types(object)
    
    default = object.portal_type in included_types
    
    if object.hasProperty('pSEO_included_in_sitemapxml'):
        return object.getProperty('pSEO_included_in_sitemapxml', default)
    return default

@indexer(IBaseContent)
def get_priority_sitemapxml(object, **kw):
    if object.hasProperty('pSEO_priority_sitemapxml'):
        return object.getProperty('pSEO_priority_sitemapxml', None)
    return None