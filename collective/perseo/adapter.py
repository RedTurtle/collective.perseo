from zope.annotation.interfaces import IAnnotations
# from Products.Archetypes.interfaces.base import IBaseContent
from plone.indexer.decorator import indexer
from pkg_resources import get_distribution
try:
    from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
except:
    from plone.app.users.browser.userdatapanel import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):

    def get_google_author(self):
        return self.context.getProperty('google_author', '')

    def set_google_author(self, value):
        return self.context.setMemberProperties({'google_author': value})

    google_author = property(get_google_author, set_google_author)

    def get_twitter_author(self):
        return self.context.getProperty('twitter_author', '')

    def set_twitter_author(self, value):
        return self.context.setMemberProperties({'twitter_author': value})

    twitter_author = property(get_twitter_author, set_twitter_author)


# @indexer(IBaseContent)
# def get_included_in_sitemapxml(object, **kw):
#     try:
#         annotations = IAnnotations(object)
#         if annotations.has_key('pSEO_included_in_sitemapxml'):
#             return annotations.get('pSEO_included_in_sitemapxml', None)
#     except:
#         return None
#     return None
#
#
# @indexer(IBaseContent)
# def get_priority_sitemapxml(object, **kw):
#     try:
#         annotations = IAnnotations(object)
#         if annotations.has_key('pSEO_priority_sitemapxml'):
#             return annotations.get('pSEO_priority_sitemapxml', None)
#     except:
#         return None
#     return None
