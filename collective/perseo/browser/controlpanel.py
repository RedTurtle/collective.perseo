from z3c.form import field
from plone.app.registry.browser import controlpanel
from plone.z3cform.fieldsets import group

from collective.perseo import perseoMessageFactory as _
from collective.perseo.interfaces import ISEOConfigSchema, \
   ISEOConfigTitleSchema, ISEOConfigSiteMapXMLSchema, ISEOConfigIndexingSchema


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


class PerSEOSettingsEditForm(controlpanel.RegistryEditForm):

    label = _(u"PerSEO settings")
    description = _(u"")
    schema = ISEOConfigSchema
    groups = (SitemapForm, IndexingForm, TitleForm,)

    def updateFields(self):
        super(PerSEOSettingsEditForm, self).updateFields()


class PerSEOControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PerSEOSettingsEditForm
