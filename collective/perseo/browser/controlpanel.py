from z3c.form import field
from plone.app.registry.browser import controlpanel
from plone.z3cform.fieldsets import group
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView

from collective.perseo import perseoMessageFactory as _
from collective.perseo.interfaces import ISEOControlpanel
from collective.perseo.interfaces.metaconfig import ISEOConfigTitleSchema
from collective.perseo.interfaces.controlpanel import ISEOConfigSiteMapXMLSchema,\
        ISEOConfigIndexingSchema, ISEOConfigSocialSchema


class TitleForm(group.Group):
    label = _(u"Type headers")
    fields = field.Fields(ISEOConfigTitleSchema)


class SitemapForm(group.Group):
    label = _(u"Sitemap")
    description = _(u"Handle how sitemap will be generated")
    fields = field.Fields(ISEOConfigSiteMapXMLSchema)


class IndexingForm(group.Group):
    label = _(u"Indexing")
    description = _(u"Handle how different types with be index by robots")
    fields = field.Fields(ISEOConfigIndexingSchema)


class SocialForm(group.Group):
    label = _(u"Social networks")
    description = _(u"Handle how your site will be indexed by social networks")
    fields = field.Fields(ISEOConfigSocialSchema)


class PerSEOSettingsEditForm(controlpanel.RegistryEditForm):

    label = _(u"PerSEO settings")
    description = _(u"")
    schema = ISEOControlpanel
    groups = (SitemapForm, IndexingForm, SocialForm, TitleForm,)

    def updateFields(self):
        super(PerSEOSettingsEditForm, self).updateFields()


class PerSEOControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PerSEOSettingsEditForm


class PerSEORSS(BrowserView):

    def __call__(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISEOControlpanel)
        return {'indexing_feed_rss':  settings.indexing_feed_rss}
