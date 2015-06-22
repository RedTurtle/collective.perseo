# -*- coding: utf-8 -*-

from zope.interface import implements

try:
    from zope.app.schema.vocabulary import IVocabularyFactory
except ImportError:
    # Plone 4.1+
    from zope.schema.interfaces import IVocabularyFactory

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from Products.CMFCore.utils import getToolByName
from zope.site.hooks import getSite


BAD_TYPES = ("ATBooleanCriterion", "ATDateCriteria", "ATDateRangeCriterion",
             "ATListCriterion", "ATPortalTypeCriterion", "ATReferenceCriterion",
             "ATSelectionCriterion", "ATSimpleIntCriterion", "Plone Site",
             "ATSimpleStringCriterion", "ATSortCriterion",
             "Discussion Item", "TempFolder", "ATCurrentAuthorCriterion",
             "ATPathCriterion", "ATRelativePathCriterion",
             'FieldsetEnd', 'FieldsetFolder', 'FieldsetStart', 'FormBooleanField',
             'FormCaptchaField', 'FormCustomScriptAdapter', 'FormDateField',
             'FormFileField', 'FormFixedPointField', 'FormIntegerField',
             'FormLabelField', 'FormLikertField', 'FormLinesField',
             'FormMailerAdapter', 'FormMapField', 'FormMultiSelectionField',
             'FormPasswordField', 'FormRichLabelField', 'FormRichTextField',
             'FormSaveData2ContentAdapter', 'FormSaveData2ContentEntry',
             'FormSaveDataAdapter', 'FormSelectionField', 'FormStringField',
             'FormTextField', 'FormThanksPage')


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
