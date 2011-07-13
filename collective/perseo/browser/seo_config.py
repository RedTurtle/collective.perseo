from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts

from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm

from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot

from collective.perseo import perseoMessageFactory as _

class ISEOConfigBaseSchema(Interface):
    """"""
class ISEOConfigAdvancedSchema(Interface):
    """"""

class ISEOConfigWMToolsSchema(Interface):
    """Schema for WebMaster Tools"""

class ISEOConfigSchema(ISEOConfigBaseSchema,
                       ISEOConfigAdvancedSchema,
                       ISEOConfigWMToolsSchema):
    """Combined schema for the adapter lookup.
    """

class SEOConfigAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(ISEOConfigSchema)

    def __init__(self, context):
        super(SEOConfigAdapter, self).__init__(context)

# Fieldset configurations
baseset = FormFieldsets(ISEOConfigBaseSchema)
baseset.id = 'seobase'
baseset.label = _(u'label_seobase', default=u'Base')

advancedset = FormFieldsets(ISEOConfigAdvancedSchema)
advancedset.id = 'seoadvanced'
advancedset.label = _(u'label_seoadvanced', default=u'Advanced')

wmtoolsset = FormFieldsets(ISEOConfigWMToolsSchema)
wmtoolsset.id = 'seowmtool'
wmtoolsset.label = _(u'label_seowmtool', default=u'WM Tools')

class SEOConfig(ControlPanelForm):

    form_fields = FormFieldsets(baseset, advancedset, wmtoolsset)

    label = _("Plone SEO Configuration")
    description = _("seo_configlet_description", default="You can select what "
                    "content types are qSEOptimizer-enabled, and control if "
                    "Dublin Core metatags are exposed in the header of content "
                    "pages.")
    form_name = _("")
