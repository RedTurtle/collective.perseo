from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName

from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from zope.site.hooks import getSite

try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass


class SortedDict(dict):
    """ A sorted dictionary.
    """
    security = ClassSecurityInfo()

    security.declarePublic('items')
    def items(self):
        primary_metatags = self.pmt
        lst = [(name,self[name]) for name in primary_metatags                    \
                                                 if name in self.keys()] +       \
              [(name, self[name]) for name in self.keys()                        \
                                                 if name not in primary_metatags]
        return lst


    security.declarePublic('__init__')
    def __init__(self, *args, **kwargs):
        super(SortedDict,self).__init__(*args, **kwargs)
        self.pmt = []


    security.declarePublic('__setitem__')
    def __setitem__(self, i, y):
        super(SortedDict,self).__setitem__(i, y)
        if i not in self.pmt:
            self.pmt.append(i)

    security.declarePublic('pop')
    def pop(self, k, *args, **kwargs):
        super(SortedDict,self).pop(k, *args, **kwargs)
        if k in self.pmt:
            self.pmt.remove(k)

try:
    InitializeClass(SortedDict)
except:
    pass


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
