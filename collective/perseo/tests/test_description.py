from collective.perseo.tests.base import PerSeoTestCase
from zope.component import queryAdapter


class TestDescription(PerSeoTestCase):

    def test_plonesite_description(self):
        portal = self.layer['portal']

        #  without homepage set
        self.assertEqual(portal.unrestrictedTraverse('@@perseo-context').perseo_description(), u'') #should be empty


class TestContentTypeDescriptions(PerSeoTestCase):

    TYPES_TO_TEST = ('event', 'file', 'folder', 'image', 'link', 'newsitem', 'topic')# 'Document')

    def test_contenttype_without_description(self):
        portal = self.layer['portal']
        for t in self.TYPES_TO_TEST:
            self.assertEqual(portal['test-%s' % t].unrestrictedTraverse('@@perseo-context').perseo_description(), u'')

    def test_contenttype_with_custom_perseo_description(self):
        portal = self.layer['portal']
        #  if we set perseo description in the context it should be different:
        for t in self.TYPES_TO_TEST:
            portal['test-%s' % t].unrestrictedTraverse('@@perseo-tab-context').setProperty('pSEO_description', u'My custom %s description' % t)
            self.assertEqual(portal['test-%s' % t].unrestrictedTraverse('@@perseo-context').perseo_description(), u'My custom %s description' % t)

        #  but we should still have original description
        for t in self.TYPES_TO_TEST:
            self.assertEqual(portal['test-%s' % t].Description(), '')

    def test_contenttype_description_after_change(self):
        portal = self.layer['portal']
        for t in self.TYPES_TO_TEST:
            portal['test-%s' % t].setDescription(u'This is a new %s description' % t)
            self.assertEqual(portal['test-%s' % t].unrestrictedTraverse('@@perseo-context').perseo_description(), u'This is a new %s description' % t)

    def test_contenttype_perseo_global_description(self):
        from collective.perseo.browser.seo_config import ISEOConfigSchema
        portal = self.layer['portal']
        gseo = queryAdapter(portal, ISEOConfigSchema)

        for t in self.TYPES_TO_TEST:
            setattr(gseo, '%s_description' % t, u'My custom %s description' % t)
            self.assertEqual(portal['test-%s' % t].unrestrictedTraverse('@@perseo-context').perseo_description(), u'My custom %s description' % t)

