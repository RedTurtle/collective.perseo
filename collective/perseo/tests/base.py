import unittest2 as unittest

from zope.interface import alsoProvides
from plone.testing import z2
from plone.app.testing import TEST_USER_NAME
from plone.app.testing import TEST_USER_PASSWORD
from collective.perseo.tests import layer
from collective.perseo.browser.interfaces import IPerSEOLayer


def get_browser(app, loggedIn=True):
    browser = z2.Browser(app)
    if loggedIn:
        auth = 'Basic %s:%s' % (TEST_USER_NAME, TEST_USER_PASSWORD)
        browser.addHeader('Authorization', auth)
    return browser


class PerSeoTestCase(unittest.TestCase):

    layer = layer.PERSEO_INTEGRATION

    def setUp(self):
        alsoProvides(self.layer['request'], IPerSEOLayer)
