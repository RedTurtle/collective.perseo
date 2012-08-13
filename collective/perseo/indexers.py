#from zope.interface import Interface
from Products.Archetypes.interfaces.base import IBaseContent
from plone.indexer.decorator import indexer
from zope.annotation.interfaces import IAnnotations

@indexer(IBaseContent)
def get_included_in_sitemapxml(object, **kw):
    try:
        annotations = IAnnotations(object)
        if 'pSEO_included_in_sitemapxml' in annotations:
            return annotations.get('pSEO_included_in_sitemapxml', None)
    except:
        return None
    return None

@indexer(IBaseContent)
def get_priority_sitemapxml(object, **kw):
    try:
        annotations = IAnnotations(object)
        if 'pSEO_priority_sitemapxml' in annotations:
            return annotations.get('pSEO_priority_sitemapxml', None)
    except:
        return None
    return None