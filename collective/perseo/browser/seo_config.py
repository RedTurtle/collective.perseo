from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from zope.schema import TextLine

from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm

from Products.CMFDefault.formlib.schema import SchemaAdapterBase, ProxyFieldProperty
from Products.CMFPlone.interfaces import IPloneSiteRoot

from collective.perseo import perseoMessageFactory as _

class ISEOConfigWMToolsSchema(Interface):
    """Schema for WebMaster Tools"""
    
    googleWebmasterTools = TextLine(
        title=_("label_googleWebmasterTools",
                default=u"Google Webmaster Tools"),
        description=u"https://www.google.com/webmasters/tools/",
        required=False)
    
    yahooSiteExplorer = TextLine(
        title=_("label_yahooSiteExplorer",
                default=u"Yahoo Site Explorer"),
        description=u"https://siteexplorer.search.yahoo.com/mysites",
        required=False)
    
    bingWebmasterTools = TextLine(
        title=_("label_bingWebmasterTools",
                default=u"Bing Webmaster Tools"),
        description=u"http://www.bing.com/webmaster/",
        required=False)
    
class ISEOConfigTitleSchema(Interface):
    """Schema for Title"""
    

class ISEOConfigSchema(ISEOConfigWMToolsSchema,
                       ISEOConfigTitleSchema):
    """Combined schema for the adapter lookup.
    """

class SEOConfigAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(ISEOConfigSchema)

    def __init__(self, context):
        super(SEOConfigAdapter, self).__init__(context)
        
    googleWebmasterTools = ProxyFieldProperty(ISEOConfigSchema['googleWebmasterTools'])
    yahooSiteExplorer = ProxyFieldProperty(ISEOConfigSchema['yahooSiteExplorer'])
    bingWebmasterTools = ProxyFieldProperty(ISEOConfigSchema['bingWebmasterTools'])

# Fieldset configurations

wmtoolsset = FormFieldsets(ISEOConfigWMToolsSchema)
wmtoolsset.id = 'seowmtools'
wmtoolsset.label = _(u'label_seowmtools', default=u'WM Tools')

titleset = FormFieldsets(ISEOConfigTitleSchema)
titleset.id = 'seotitle'
titleset.label = _(u'label_seotitle', default=u'Title')

class PerSEOConfig(ControlPanelForm):

    form_fields = FormFieldsets(wmtoolsset, titleset)

    label = _("Plone SEO Configuration")
    description = _("seo_configlet_description", default="You can select what "
                    "content types are qSEOptimizer-enabled, and control if "
                    "Dublin Core metatags are exposed in the header of content "
                    "pages.")
    form_name = _("")
