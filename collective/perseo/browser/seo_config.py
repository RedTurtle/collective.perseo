from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from zope.schema import TextLine, Text

from zope.app.form.browser import TextAreaWidget, TextWidget

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
    
    homepage_title = TextLine(
        title=_("label_homepage_title",
                default=u"Home Page Title"),
        required=False)
    
    homepage_description = Text(
        title=_("label_homepage_description",
                default=u"Home Page Description"),
        required=False)
    
    homepage_keywords = TextLine(
        title=_("label_homepage_keywords",
                default=u"Home Page Keywords"),
        required=False)
    
    singlepage_title = TextLine(
        title=_("label_singlepage_title",
                default=u"Single Page Title"),
        required=False)
    
    singlepage_description = Text(
        title=_("label_singlepage_description",
                default=u"Single Page Description"),
        required=False)
    
    singlepage_keywords = TextLine(
        title=_("label_singlepage_keywords",
                default=u"Single Page Keywords"),
        required=False)
    

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
    homepage_title = ProxyFieldProperty(ISEOConfigSchema['homepage_title'])
    homepage_description = ProxyFieldProperty(ISEOConfigSchema['homepage_description'])
    homepage_keywords = ProxyFieldProperty(ISEOConfigSchema['homepage_keywords'])
    singlepage_title = ProxyFieldProperty(ISEOConfigSchema['singlepage_title'])
    singlepage_description = ProxyFieldProperty(ISEOConfigSchema['singlepage_description'])
    singlepage_keywords = ProxyFieldProperty(ISEOConfigSchema['singlepage_keywords'])

# Fieldset configurations

wmtoolsset = FormFieldsets(ISEOConfigWMToolsSchema)
wmtoolsset.id = 'seowmtools'
wmtoolsset.label = _(u'label_seowmtools', default=u'WM Tools')

titleset = FormFieldsets(ISEOConfigTitleSchema)
titleset.id = 'seotitle'
titleset.label = _(u'label_seotitle', default=u'Title')

class PerSEOConfig(ControlPanelForm):

    form_fields = FormFieldsets(wmtoolsset, titleset)
    
    form_fields['googleWebmasterTools'].custom_widget = TextWidget
    form_fields['yahooSiteExplorer'].custom_widget = TextWidget
    form_fields['bingWebmasterTools'].custom_widget = TextWidget
    form_fields['homepage_title'].custom_widget = TextWidget
    form_fields['homepage_description'].custom_widget = TextAreaWidget
    form_fields['homepage_description'].custom_widget.height = 3
    form_fields['homepage_keywords'].custom_widget = TextWidget
    form_fields['singlepage_title'].custom_widget = TextWidget
    form_fields['singlepage_description'].custom_widget = TextAreaWidget
    form_fields['singlepage_description'].custom_widget.height = 3
    form_fields['singlepage_keywords'].custom_widget = TextWidget

    label = _("Plone SEO Configuration")
    description = _("seo_configlet_description", default="You can select what "
                    "content types are qSEOptimizer-enabled, and control if "
                    "Dublin Core metatags are exposed in the header of content "
                    "pages.")
    form_name = _("")
