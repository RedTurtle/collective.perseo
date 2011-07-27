from zope.interface import Interface
from plone.indexer.decorator import indexer

@indexer(Interface)
def get_included_in_sitemapxml(object, **kw):
    if object.hasProperty('pSEO_included_in_sitemapxml'):
        return object.getProperty('pSEO_included_in_sitemapxml', True)
    return True