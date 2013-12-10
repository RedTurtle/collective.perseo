from Products.CMFCore.utils import getToolByName

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
try:
    # Plone < 4.3
    from zope.app.component.hooks import getSite
except ImportError:
    # Plone >= 4.3
    from zope.component.hooks import getSite  # NOQA

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
