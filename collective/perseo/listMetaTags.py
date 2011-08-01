from collective.perseo.browser.viewlets import METATAGS
from Products.CMFPlone.PloneTool import PloneTool

originalListMetaTags = PloneTool.listMetaTags


def perSEOListMetaTags(self, context):
    """ Custom listMetaTags method
    """
    from collective.perseo.browser.interfaces import IPerSEOLayer
    if not IPerSEOLayer.providedBy(self.REQUEST):
        return originalListMetaTags(self, context)
    
    list_meta_tags = originalListMetaTags(self, context)
    
    for key in METATAGS.keys():
        if list_meta_tags.has_key(key):
            list_meta_tags.pop(key)

    return list_meta_tags
