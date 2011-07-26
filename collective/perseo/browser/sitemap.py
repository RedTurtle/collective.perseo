from plone.app.layout.sitemap.sitemap import SiteMapView
from Products.CMFCore.utils import getToolByName

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite

class PerSEOSiteMapView (SiteMapView):
    """Creates the sitemap as explained in the specifications.

    http://www.sitemaps.org/protocol.php
    """

    def objects(self):
        """Returns the data to create the sitemap."""
        
        catalog = getToolByName(self.context, 'portal_catalog')
        for item in catalog.searchResults({'Language': 'all'}):
            yield {
                'loc': item.getURL(),
                'lastmod': item.modified.ISO8601(),
                #'changefreq': 'always', # hourly/daily/weekly/monthly/yearly/never
                #'prioriy': 0.5, # 0.0 to 1.0
            }

BAD_TYPES = ("ATBooleanCriterion", "ATDateCriteria", "ATDateRangeCriterion",
             "ATListCriterion", "ATPortalTypeCriterion", "ATReferenceCriterion",
             "ATSelectionCriterion", "ATSimpleIntCriterion", "Plone Site",
             "ATSimpleStringCriterion", "ATSortCriterion",
             "Discussion Item", "TempFolder", "ATCurrentAuthorCriterion",
             "ATPathCriterion", "ATRelativePathCriterion", )

class ReallyUserFriendlyTypesVocabulary(object):
    """Vocabulary factory for really user friendly portal types.
    """
    implements(IVocabularyFactory)

    def __call__(self, context):
        site = getSite()
        ttool = getToolByName(site, 'portal_types', None)
        if ttool is None:
            return SimpleVocabulary([])
        items = [SimpleTerm(t, t, ttool[t].Title())
                 for t in ttool.listContentTypes()
                 if t not in BAD_TYPES]
        return SimpleVocabulary(items)

ReallyUserFriendlyTypesVocabularyFactory = ReallyUserFriendlyTypesVocabulary()