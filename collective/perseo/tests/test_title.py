from collective.perseo.tests.base import PerSeoTestCase


class TestTitle(PerSeoTestCase):

    def test_plonesite_title(self):
        portal = self.layer['portal']

        #  without homepage set
        self.assertEqual(portal.unrestrictedTraverse('@@perseo-context').perseo_title(), u'Plone site')

    def test_document_title(self):
        portal = self.layer['portal']
        self.assertEqual(portal['test-page'].unrestrictedTraverse('@@perseo-context').perseo_title(), u'test-page')

    def test_document_custom_perseo_title(self):
        portal = self.layer['portal']
        #  if we set perseo title in test-page it should be different:
        portal['test-page'].unrestrictedTraverse('@@perseo-tab-context').setProperty('pSEO_title', u'My custom page title')
        self.assertEqual(portal['test-page'].unrestrictedTraverse('@@perseo-context').perseo_title(), u'My custom page title')

        #  but we should still have original title
        self.assertEqual(portal['test-page'].title_or_id(), 'test-page')

    def test_folder_title(self):
        portal = self.layer['portal']
        self.assertEqual(portal['test-folder'].unrestrictedTraverse('@@perseo-context').perseo_title(), u'test-folder')

    def test_folder_title_after_change(self):
        portal = self.layer['portal']
        portal['test-folder'].setTitle(u'This is a new folder title')
        self.assertEqual(portal['test-folder'].unrestrictedTraverse('@@perseo-context').perseo_title(), u'This is a new folder title')

    def test_collection_title(self):
        portal = self.layer['portal']
        self.assertEqual(portal['test-collection'].unrestrictedTraverse('@@perseo-context').perseo_title(), u'test-collection')

    def test_newsitem_title(self):
        portal = self.layer['portal']
        self.assertEqual(portal['test-newsitem'].unrestrictedTraverse('@@perseo-context').perseo_title(), u'test-newsitem')




