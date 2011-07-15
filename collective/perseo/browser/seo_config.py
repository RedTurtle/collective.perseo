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
    
    searchpage_title = TextLine(
        title=_("label_searchpage_title",
                default=u"Search Page Title"),
        required=False)
    
    searchpage_description = Text(
        title=_("label_searchpage_description",
                default=u"Search Page Description"),
        required=False)
    
    searchpage_keywords = TextLine(
        title=_("label_searchpage_keywords",
                default=u"Search Page Keywords"),
        required=False)
    
    notfoundpage_title = TextLine(
        title=_("label_notfoundpage_title",
                default=u"Not Found Page Title"),
        required=False)
    
    notfoundpage_description = Text(
        title=_("label_notfoundpage_description",
                default=u"Not Found Page Description"),
        required=False)
    
    notfoundpage_keywords = TextLine(
        title=_("label_notfoundpage_keywords",
                default=u"Not Found Page Keywords"),
        required=False)
    
    authorpage_title = TextLine(
        title=_("label_authorpage_title",
                default=u"Author Page Title"),
        required=False)
    
    authorpage_description = Text(
        title=_("label_authorpage_description",
                default=u"Author Page Description"),
        required=False)
    
    authorpage_keywords = TextLine(
        title=_("label_authorpage_keywords",
                default=u"Author Page Keywords"),
        required=False)
    
    sitemappage_title = TextLine(
        title=_("label_sitemappage_title",
                default=u"Site map Title"),
        required=False)
    
    sitemappage_description = Text(
        title=_("label_sitemappage_description",
                default=u"Site map Description"),
        required=False)
    
    sitemappage_keywords = TextLine(
        title=_("label_sitemappage_keywords",
                default=u"Site map Keywords"),
        required=False)
    
    accessibilitypage_title = TextLine(
        title=_("label_accessibilitypage_title",
                default=u"Accessibility Title"),
        required=False)
    
    accessibilitypage_description = Text(
        title=_("label_accessibilitypage_description",
                default=u"Accessibility Description"),
        required=False)
    
    accessibilitypage_keywords = TextLine(
        title=_("label_accessibilitypage_keywords",
                default=u"Accessibility Keywords"),
        required=False)
    
    contactpage_title = TextLine(
        title=_("label_contactpage_title",
                default=u"Contact Title"),
        required=False)
    
    contactpage_description = Text(
        title=_("label_contactpage_description",
                default=u"Contact Description"),
        required=False)
    
    contactpage_keywords = TextLine(
        title=_("label_contactpage_keywords",
                default=u"Contact Keywords"),
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
    searchpage_title = ProxyFieldProperty(ISEOConfigSchema['searchpage_title'])
    searchpage_description = ProxyFieldProperty(ISEOConfigSchema['searchpage_description'])
    searchpage_keywords = ProxyFieldProperty(ISEOConfigSchema['searchpage_keywords'])
    notfoundpage_title = ProxyFieldProperty(ISEOConfigSchema['notfoundpage_title'])
    notfoundpage_description = ProxyFieldProperty(ISEOConfigSchema['notfoundpage_description'])
    notfoundpage_keywords = ProxyFieldProperty(ISEOConfigSchema['notfoundpage_keywords'])
    authorpage_title = ProxyFieldProperty(ISEOConfigSchema['authorpage_title'])
    authorpage_description = ProxyFieldProperty(ISEOConfigSchema['authorpage_description'])
    authorpage_keywords = ProxyFieldProperty(ISEOConfigSchema['authorpage_keywords'])
    sitemappage_title = ProxyFieldProperty(ISEOConfigSchema['sitemappage_title'])
    sitemappage_description = ProxyFieldProperty(ISEOConfigSchema['sitemappage_description'])
    sitemappage_keywords = ProxyFieldProperty(ISEOConfigSchema['sitemappage_keywords'])
    accessibilitypage_title = ProxyFieldProperty(ISEOConfigSchema['accessibilitypage_title'])
    accessibilitypage_description = ProxyFieldProperty(ISEOConfigSchema['accessibilitypage_description'])
    accessibilitypage_keywords = ProxyFieldProperty(ISEOConfigSchema['accessibilitypage_keywords'])
    contactpage_title = ProxyFieldProperty(ISEOConfigSchema['contactpage_title'])
    contactpage_description = ProxyFieldProperty(ISEOConfigSchema['contactpage_description'])
    contactpage_keywords = ProxyFieldProperty(ISEOConfigSchema['contactpage_keywords'])

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
    form_fields['searchpage_title'].custom_widget = TextWidget
    form_fields['searchpage_description'].custom_widget = TextAreaWidget
    form_fields['searchpage_description'].custom_widget.height = 3
    form_fields['searchpage_keywords'].custom_widget = TextWidget
    form_fields['notfoundpage_title'].custom_widget = TextWidget
    form_fields['notfoundpage_description'].custom_widget = TextAreaWidget
    form_fields['notfoundpage_description'].custom_widget.height = 3
    form_fields['notfoundpage_keywords'].custom_widget = TextWidget
    form_fields['authorpage_title'].custom_widget = TextWidget
    form_fields['authorpage_description'].custom_widget = TextAreaWidget
    form_fields['authorpage_description'].custom_widget.height = 3
    form_fields['authorpage_keywords'].custom_widget = TextWidget
    form_fields['sitemappage_title'].custom_widget = TextWidget
    form_fields['sitemappage_description'].custom_widget = TextAreaWidget
    form_fields['sitemappage_description'].custom_widget.height = 3
    form_fields['sitemappage_keywords'].custom_widget = TextWidget
    form_fields['accessibilitypage_title'].custom_widget = TextWidget
    form_fields['accessibilitypage_description'].custom_widget = TextAreaWidget
    form_fields['accessibilitypage_description'].custom_widget.height = 3
    form_fields['accessibilitypage_keywords'].custom_widget = TextWidget
    form_fields['contactpage_title'].custom_widget = TextWidget
    form_fields['contactpage_description'].custom_widget = TextAreaWidget
    form_fields['contactpage_description'].custom_widget.height = 3
    form_fields['contactpage_keywords'].custom_widget = TextWidget

    label = _("Plone SEO Configuration")
    description = _("seo_configlet_description", default="You can select what "
                    "content types are qSEOptimizer-enabled, and control if "
                    "Dublin Core metatags are exposed in the header of content "
                    "pages.")
    form_name = _("")
