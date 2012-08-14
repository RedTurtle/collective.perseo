from zope.configuration import xmlconfig
from plone.testing import z2
from plone.app.testing import PloneFixture
from plone.app.testing import PloneTestLifecycle
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID


class PerSeoFixture(PloneFixture):

    # No sunburst please
    extensionProfiles = ()

PERSEO_FIXTURE = PerSeoFixture()


class PerSeoTestLifecycle(PloneTestLifecycle):

    defaultBases = (PERSEO_FIXTURE, )


class IntegrationTesting(PerSeoTestLifecycle, z2.IntegrationTesting):
    pass


class PerSeoLayer(PloneSandboxLayer):
    """ layer for integration tests """

    defaultBases = (PERSEO_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        import collective.perseo

        xmlconfig.file("configure.zcml", collective.perseo,
                       context=configurationContext)

        z2.installProduct(app, 'collective.js.jqueryui')
        z2.installProduct(app, 'collective.perseo')

    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'collective.perseo')
        z2.uninstallProduct(app, 'collective.js.jqueryui')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.perseo:default')

        setRoles(portal, TEST_USER_ID, ['Manager'])

        portal.invokeFactory('Document', 'test-document')
        portal.invokeFactory('Folder', 'test-folder')
        portal.invokeFactory('Collection', 'test-collection')
        portal.invokeFactory('News Item', 'test-newsitem')
        portal.invokeFactory('Event', 'test-event')
        portal.invokeFactory('Image', 'test-image')
        portal.invokeFactory('File', 'test-file')
        portal.invokeFactory('Link', 'test-link')
        portal.portal_types['Topic'].global_allow = True
        portal.invokeFactory('Topic', 'test-topic')

        # don't require secure cookies in tests
        portal.acl_users.session.secure = False
        setRoles(portal, TEST_USER_ID, ['Member'])


PERSEO_LAYER = PerSeoLayer()
PERSEO_INTEGRATION = IntegrationTesting(
    bases=(PERSEO_LAYER, ), name="PerSeo:Integration")

