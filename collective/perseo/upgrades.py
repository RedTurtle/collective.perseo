import logging
from Products.CMFCore.utils import getToolByName
from zope.annotation.interfaces import IAnnotations
from zope.component import queryMultiAdapter

logger = logging.getLogger('collective.perseo')
REMOVE_SEOPROPERTIES = ['pSEO_title',
                        'pSEO_description',
                        'pSEO_keywords',
                        'pSEO_robots_advanced',
                        'pSEO_robots_follow',
                        'pSEO_robots_index',
                        'pSEO_canonical',
                        'pSEO_included_in_sitemapxml',
                        'pSEO_priority_sitemapxml',
                        'pSEO_itemtype']

def toAnnotation(obj):
    for property in REMOVE_SEOPROPERTIES:
        if obj.hasProperty(property):
            value = obj.getProperty(property,None)
            if type(value) == type(()): value = list(value)
            obj.manage_delProperties([property])
            annotations = IAnnotations(obj)
            annotations[property] = value
            msg = "Migrate property %(property)s to annotation, for object %(object)s"
            logger.log(logging.INFO, msg % {'object':obj.id,'property':property} )

def migrationPropertyToAnnotation(portal):
    toAnnotation(portal)
    catalog = getToolByName(portal, 'portal_catalog')
    for item in catalog.searchResults():
        toAnnotation(item.getObject())

def upgrade_1_to_2(setuptool):
    """ Upgrade Collective perSEO 0.1 to 0.2
    """
    pps = queryMultiAdapter((setuptool, setuptool.REQUEST), name="plone_portal_state")
    migrationPropertyToAnnotation(pps.portal())
    