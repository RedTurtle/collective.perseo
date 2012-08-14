from collective.perseo.tests.base import PerSeoTestCase
from zope.component import queryAdapter


class TestTitle(PerSeoTestCase):

    def test_plonesite_title(self):
        portal = self.layer['portal']

        #  without homepage set
        self.assertEqual(portal.unrestrictedTraverse('@@perseo-context').perseo_title(), u'Plone site')


class TestContentTypeTitles(PerSeoTestCase):

    TYPES_TO_TEST = ('event', 'file', 'folder', 'image', 'link', 'newsitem',)# 'Document', 'Topic')

    def test_contenttype_without_title(self):
        portal = self.layer['portal']
        for t in self.TYPES_TO_TEST:
            self.assertEqual(portal['test-%s' % t].unrestrictedTraverse('@@perseo-context').perseo_title(), u'test-%s' % t)

    def test_contenttype_with_custom_perseo_title(self):
        portal = self.layer['portal']
        #  if we set perseo title in the context it should be different:
        for t in self.TYPES_TO_TEST:
            portal['test-%s' % t].unrestrictedTraverse('@@perseo-tab-context').setProperty('pSEO_title', u'My custom %s title' % t)
            self.assertEqual(portal['test-%s' % t].unrestrictedTraverse('@@perseo-context').perseo_title(), u'My custom %s title' % t)

        #  but we should still have original title
        for t in self.TYPES_TO_TEST:
            self.assertEqual(portal['test-%s' % t].title_or_id(), 'test-%s' % t)

    def test_contenttype_title_after_change(self):
        portal = self.layer['portal']
        for t in self.TYPES_TO_TEST:
            portal['test-%s' % t].setTitle(u'This is a new %s title' % t)
            self.assertEqual(portal['test-%s' % t].unrestrictedTraverse('@@perseo-context').perseo_title(), u'This is a new %s title' % t)

    def test_contenttype_perseo_global_title(self):
        from collective.perseo.browser.seo_config import ISEOConfigSchema
        portal = self.layer['portal']
        gseo = queryAdapter(portal, ISEOConfigSchema)

        for t in self.TYPES_TO_TEST:
            setattr(gseo, '%s_title' % t, u'My custom %s title' % t)
            self.assertEqual(portal['test-%s' % t].unrestrictedTraverse('@@perseo-context').perseo_title(), u'My custom %s title' % t)

