from zope.annotation.interfaces import IAnnotations
from Products.Archetypes.interfaces.base import IBaseContent
from plone.indexer.decorator import indexer
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    def get_google_author(self):
        return self.context.getProperty('google_author', '')
    def set_google_author(self, value):
        return self.context.setMemberProperties({'google_author': value})
    google_author = property(get_google_author, set_google_author)


@indexer(IBaseContent)
def get_included_in_sitemapxml(object, **kw):
    try:
        annotations = IAnnotations(object)
        if annotations.has_key('pSEO_included_in_sitemapxml'):
            return annotations.get('pSEO_included_in_sitemapxml', None)
    except:
        return None
    return None


@indexer(IBaseContent)
def get_priority_sitemapxml(object, **kw):
    try:
        annotations = IAnnotations(object)
        if annotations.has_key('pSEO_priority_sitemapxml'):
            return annotations.get('pSEO_priority_sitemapxml', None)
    except:
        return None
    return None
