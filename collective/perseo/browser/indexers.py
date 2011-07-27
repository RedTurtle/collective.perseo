#from zope.interface import Interface
from Products.Archetypes.interfaces.base import IBaseContent
from plone.indexer.decorator import indexer

@indexer(IBaseContent)
def get_included_in_sitemapxml(object, **kw):
    if object.hasProperty('pSEO_included_in_sitemapxml'):
        return object.getProperty('pSEO_included_in_sitemapxml', True)
    return True

@indexer(IBaseContent)
def get_priority_sitemapxml(object, **kw):
    if object.hasProperty('pSEO_priority_sitemapxml'):
        return object.getProperty('pSEO_priority_sitemapxml', None)
    return None