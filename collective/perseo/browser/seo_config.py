import re
from zope.interface import Interface
from zope.interface import implements
from zope.component import adapts
from zope.schema import TextLine, Text, List, Bool, Tuple, Choice

from zope.app.component.hooks import getSite
from zope.app.form.browser import TextAreaWidget, TextWidget#, CheckBoxWidget

from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.widgets import MultiCheckBoxThreeColumnWidget

from Products.CMFDefault.formlib.schema import SchemaAdapterBase, ProxyFieldProperty
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName, safe_unicode

from collective.perseo import perseoMessageFactory as _
from collective.perseo.browser.sitemap import BAD_TYPES

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
    
    tracking_code_header = Text(
        title=_("label_tracking_code_header",
                default=u"Tracking Code Header"),
        required=False)
    
    tracking_code_footer = Text(
        title=_("label_tracking_code_footer",
                default=u"Tracking Code Footer"),
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
    
    homepage_keywords = List(
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
    
    singlepage_keywords = List(
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
    
    searchpage_keywords = List(
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
    
    notfoundpage_keywords = List(
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
    
    authorpage_keywords = List(
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
    
    sitemappage_keywords = List(
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
    
    accessibilitypage_keywords = List(
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
    
    contactpage_keywords = List(
        title=_("label_contactpage_keywords",
                default=u"Contact Keywords"),
        required=False)
    
    event_title = TextLine(
        title=_("label_event_title",
                default=u"Event Title"),
        required=False)
    
    event_description = Text(
        title=_("label_event_description",
                default=u"Event Description"),
        required=False)
    
    event_keywords = List(
        title=_("label_event_keywords",
                default=u"Event Keywords"),
        required=False)
    
    file_title = TextLine(
        title=_("label_file_title",
                default=u"File Title"),
        required=False)
    
    file_description = Text(
        title=_("label_file_description",
                default=u"File Description"),
        required=False)
    
    file_keywords = List(
        title=_("label_file_keywords",
                default=u"File Keywords"),
        required=False)
    
    folder_title = TextLine(
        title=_("label_folder_title",
                default=u"Folder Title"),
        required=False)
    
    folder_description = Text(
        title=_("label_folder_description",
                default=u"Folder Description"),
        required=False)
    
    folder_keywords = List(
        title=_("label_folder_keywords",
                default=u"Folder Keywords"),
        required=False)
    
    image_title = TextLine(
        title=_("label_image_title",
                default=u"Image Title"),
        required=False)
    
    image_description = Text(
        title=_("label_image_description",
                default=u"Image Description"),
        required=False)
    
    image_keywords = List(
        title=_("label_image_keywords",
                default=u"Image Keywords"),
        required=False)
    
    link_title = TextLine(
        title=_("label_link_title",
                default=u"Link Title"),
        required=False)
    
    link_description = Text(
        title=_("label_link_description",
                default=u"Link Description"),
        required=False)
    
    link_keywords = List(
        title=_("label_link_keywords",
                default=u"Link Keywords"),
        required=False)
    
    newsItem_title = TextLine(
        title=_("label_newsItem_title",
                default=u"NewsItem Title"),
        required=False)
    
    newsItem_description = Text(
        title=_("label_newsItem_description",
                default=u"NewsItem Description"),
        required=False)
    
    newsItem_keywords = List(
        title=_("label_newsItem_keywords",
                default=u"NewsItem Keywords"),
        required=False)
    
    topic_title = TextLine(
        title=_("label_topic_title",
                default=u"Topic Title"),
        required=False)
    
    topic_description = Text(
        title=_("label_topic_description",
                default=u"Topic Description"),
        required=False)
    
    topic_keywords = List(
        title=_("label_topic_keywords",
                default=u"Topic Keywords"),
        required=False)
    
class ISEOConfigIndexingSchema(Interface):
    """Schema for Indexing"""
    
    indexing_searchpage = Bool(
        title=_("label_search_page",
                default=u"Search pages"),
        default=False,
        required=False)
    
    indexing_loginregistrationpage = Bool(
        title=_("label_login_registration_page",
                default=u"Login and Registration pages"),
        default=False,
        required=False)
    
    indexing_administrationpage = Bool(
        title=_("label_administration_page",
                default=u"Administration pages"),
        default=False,
        required=False)
    
    indexing_page = Bool(
        title=_("label_single_pages",
                default=u"Single Pages"),
        default=False,
        required=False)
    
    indexing_event = Bool(
        title=_("label_indexing_event",
                default=u"Event"),
        default=False,
        required=False)
    
    indexing_file = Bool(
        title=_("label_indexing_file",
                default=u"File"),
        default=False,
        required=False)
    
    indexing_folder = Bool(
        title=_("label_indexing_folder",
                default=u"Folder"),
        default=False,
        required=False)
    
    indexing_image = Bool(
        title=_("label_indexing_image",
                default=u"Image"),
        default=False,
        required=False)
    
    indexing_link = Bool(
        title=_("label_indexing_link",
                default=u"Link"),
        default=False,
        required=False)
    
    indexing_newsItem = Bool(
        title=_("label_indexing_newsItem",
                default=u"NewsItem"),
        default=False,
        required=False)
    
    indexing_topic = Bool(
        title=_("label_indexing_topic",
                default=u"Topic"),
        default=False,
        required=False)
    
    robots_noodp = Bool(
        title=_("label_robots_noodp",
                default=u"Add noodp in whole site"),
        default=False,
        required=False)
    
    robots_noydir = Bool(
        title=_("label_robots_noydir",
                default=u"Add noydir in whole site"),
        default=False,
        required=False)
    
    robots_noarchive = Bool(
        title=_("label_robots_noarchive",
                default=u"Add noarchive in whole site"),
        default=False,
        required=False)
    
    robots_nosnippet = Bool(
        title=_("label_robots_nosnippet",
                default=u"Add nosnippet in whole site"),
        default=False,
        required=False)
    
class ISEOConfigSiteMapXMLSchema(Interface):
    """Schema for Site Map XML Tools"""
    
    not_displayed_types = Tuple(
        title=_("label_displayed_types",
                default=u"Types of content included in the XML Site Map"),
        description=_("help_displayed_types",
                      default=u"The content types that should be included in the sitemap.xml.gz."),
        required=False,
        missing_value=tuple(),
        value_type=Choice(
            vocabulary="collective.perseo.vocabularies.ReallyUserFriendlyTypes")
        )
        

class ISEOConfigSchema(ISEOConfigWMToolsSchema,
                       ISEOConfigTitleSchema,
                       ISEOConfigIndexingSchema,
                       ISEOConfigSiteMapXMLSchema):
    """Combined schema for the adapter lookup.
    """

class SEOConfigAdapter(SchemaAdapterBase):

    adapts(IPloneSiteRoot)
    implements(ISEOConfigSchema)

    def __init__(self, context):
        super(SEOConfigAdapter, self).__init__(context)
        portal = getSite()
        self.portal_types = getToolByName(portal, 'portal_types')
        portal_properties = getToolByName(portal, 'portal_properties')
        site_properties = portal_properties.site_properties
        self.encoding = site_properties.default_charset
        self.navtree_properties = portal_properties.navtree_properties
        
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
    event_title = ProxyFieldProperty(ISEOConfigSchema['event_title'])
    event_description = ProxyFieldProperty(ISEOConfigSchema['event_description'])
    event_keywords = ProxyFieldProperty(ISEOConfigSchema['event_keywords'])
    file_title = ProxyFieldProperty(ISEOConfigSchema['file_title'])
    file_description = ProxyFieldProperty(ISEOConfigSchema['file_description'])
    file_keywords = ProxyFieldProperty(ISEOConfigSchema['file_keywords']) 
    folder_title = ProxyFieldProperty(ISEOConfigSchema['folder_title'])
    folder_description = ProxyFieldProperty(ISEOConfigSchema['folder_description'])
    folder_keywords = ProxyFieldProperty(ISEOConfigSchema['folder_keywords'])
    image_title = ProxyFieldProperty(ISEOConfigSchema['image_title'])
    image_description = ProxyFieldProperty(ISEOConfigSchema['image_description'])
    image_keywords = ProxyFieldProperty(ISEOConfigSchema['image_keywords'])
    link_title = ProxyFieldProperty(ISEOConfigSchema['link_title'])
    link_description = ProxyFieldProperty(ISEOConfigSchema['link_description'])
    link_keywords = ProxyFieldProperty(ISEOConfigSchema['link_keywords'])
    newsItem_title = ProxyFieldProperty(ISEOConfigSchema['newsItem_title'])
    newsItem_description = ProxyFieldProperty(ISEOConfigSchema['newsItem_description'])
    newsItem_keywords = ProxyFieldProperty(ISEOConfigSchema['newsItem_keywords'])
    topic_title = ProxyFieldProperty(ISEOConfigSchema['topic_title'])
    topic_description = ProxyFieldProperty(ISEOConfigSchema['topic_description'])
    topic_keywords = ProxyFieldProperty(ISEOConfigSchema['topic_keywords'])
    robots_noodp = ProxyFieldProperty(ISEOConfigSchema['robots_noodp'])
    robots_noydir = ProxyFieldProperty(ISEOConfigSchema['robots_noydir'])
    robots_noarchive = ProxyFieldProperty(ISEOConfigSchema['robots_noarchive'])
    robots_nosnippet = ProxyFieldProperty(ISEOConfigSchema['robots_nosnippet'])
    indexing_searchpage = ProxyFieldProperty(ISEOConfigSchema['indexing_searchpage'])
    indexing_loginregistrationpage = ProxyFieldProperty(ISEOConfigSchema['indexing_loginregistrationpage'])
    indexing_administrationpage = ProxyFieldProperty(ISEOConfigSchema['indexing_administrationpage'])
    indexing_page = ProxyFieldProperty(ISEOConfigSchema['indexing_page'])
    indexing_event = ProxyFieldProperty(ISEOConfigSchema['indexing_event'])
    indexing_file = ProxyFieldProperty(ISEOConfigSchema['indexing_file'])
    indexing_folder = ProxyFieldProperty(ISEOConfigSchema['indexing_folder'])
    indexing_image = ProxyFieldProperty(ISEOConfigSchema['indexing_image'])
    indexing_link = ProxyFieldProperty(ISEOConfigSchema['indexing_link'])
    indexing_newsItem = ProxyFieldProperty(ISEOConfigSchema['indexing_newsItem'])
    indexing_topic = ProxyFieldProperty(ISEOConfigSchema['indexing_topic'])
    
    def getTrackingCodeHeader(self):
        tracking_code_header = getattr(self.context, 'tracking_code_header', u'')
        return safe_unicode(tracking_code_header)

    def setTrackingCodeHeader(self, value):
        if value is not None:
            self.context.tracking_code_header = value.encode(self.encoding)
        else:
            self.context.tracking_code_header = ''
            
    def getTrackingCodeFooter(self):
        tracking_code_footer = getattr(self.context, 'tracking_code_footer', u'')
        return safe_unicode(tracking_code_footer)

    def setTrackingCodeFooter(self, value):
        if value is not None:
            self.context.tracking_code_footer = value.encode(self.encoding)
        else:
            self.context.tracking_code_footer = ''
            
    tracking_code_header = property(getTrackingCodeHeader, setTrackingCodeHeader)
    tracking_code_footer = property(getTrackingCodeFooter, setTrackingCodeFooter)
    
    def getDisplayedTypes(self):
        not_displayed_types = getattr(self.context, 'not_displayed_types', ())
        
        return [t for t in self.portal_types.listContentTypes()
                        if t not in not_displayed_types and
                           t not in BAD_TYPES]

    def setNotDisplayedTypes(self, value):
        # The menu pretends to be a whitelist, but we are storing a blacklist so that
        # new types are searchable by default. Inverse the list.
        allTypes = self.portal_types.listContentTypes()

        blacklistedTypes = [t for t in allTypes if t not in value
                                                and t not in BAD_TYPES]
        self.context.not_displayed_types = blacklistedTypes

    not_displayed_types = property(getDisplayedTypes, setNotDisplayedTypes)

# Fieldset configurations

wmtoolsset = FormFieldsets(ISEOConfigWMToolsSchema)
wmtoolsset.id = 'seowmtools'
wmtoolsset.label = _(u'label_seowmtools', default=u'WM Tools')

titleset = FormFieldsets(ISEOConfigTitleSchema)
titleset.id = 'seotitle'
titleset.label = _(u'label_seotitle', default=u'Title')

indexingset = FormFieldsets(ISEOConfigIndexingSchema)
indexingset.id = 'seoindexing'
indexingset.label = _(u'label_seoindexing', default=u'Indexing')
indexingset.description = _(u'description_seoindexing', default=u"By selecting the options below" \
                                " you decide to disable the indexing of resources using noindex and nofollow.")

sitemapxmlset = FormFieldsets(ISEOConfigSiteMapXMLSchema)
sitemapxmlset.id = 'seositemapxml'
sitemapxmlset.label = _(u'label_seositemapxml', default=u'Site Map')


class Text2ListWidget(TextAreaWidget):
    height = 2
    splitter = re.compile(u'\\r?\\n', re.S|re.U)

    def _toFieldValue(self, input):
        if input == self._missing:
            return self.context._type()
        else:
            return self.context._type(filter(None, self.splitter.split(input)))

    def _toFormValue(self, value):
        if value == self.context.missing_value or value == self.context._type(): 
            return self._missing
        else:
            return u'\r\n'.join(list(value))

class PerSEOConfig(ControlPanelForm):

    form_fields = FormFieldsets(wmtoolsset, titleset, indexingset, sitemapxmlset)
    
    form_fields['googleWebmasterTools'].custom_widget = TextWidget
    form_fields['yahooSiteExplorer'].custom_widget = TextWidget
    form_fields['bingWebmasterTools'].custom_widget = TextWidget
    form_fields['homepage_title'].custom_widget = TextWidget
    form_fields['homepage_description'].custom_widget = TextAreaWidget
    form_fields['homepage_description'].custom_widget.height = 3
    form_fields['homepage_keywords'].custom_widget = Text2ListWidget
    form_fields['singlepage_title'].custom_widget = TextWidget
    form_fields['singlepage_description'].custom_widget = TextAreaWidget
    form_fields['singlepage_description'].custom_widget.height = 3
    form_fields['singlepage_keywords'].custom_widget = Text2ListWidget
    form_fields['searchpage_title'].custom_widget = TextWidget
    form_fields['searchpage_description'].custom_widget = TextAreaWidget
    form_fields['searchpage_description'].custom_widget.height = 3
    form_fields['searchpage_keywords'].custom_widget = Text2ListWidget
    form_fields['notfoundpage_title'].custom_widget = TextWidget
    form_fields['notfoundpage_description'].custom_widget = TextAreaWidget
    form_fields['notfoundpage_description'].custom_widget.height = 3
    form_fields['notfoundpage_keywords'].custom_widget = Text2ListWidget
    form_fields['authorpage_title'].custom_widget = TextWidget
    form_fields['authorpage_description'].custom_widget = TextAreaWidget
    form_fields['authorpage_description'].custom_widget.height = 3
    form_fields['authorpage_keywords'].custom_widget = Text2ListWidget
    form_fields['sitemappage_title'].custom_widget = TextWidget
    form_fields['sitemappage_description'].custom_widget = TextAreaWidget
    form_fields['sitemappage_description'].custom_widget.height = 3
    form_fields['sitemappage_keywords'].custom_widget = Text2ListWidget
    form_fields['accessibilitypage_title'].custom_widget = TextWidget
    form_fields['accessibilitypage_description'].custom_widget = TextAreaWidget
    form_fields['accessibilitypage_description'].custom_widget.height = 3
    form_fields['accessibilitypage_keywords'].custom_widget = Text2ListWidget
    form_fields['contactpage_title'].custom_widget = TextWidget
    form_fields['contactpage_description'].custom_widget = TextAreaWidget
    form_fields['contactpage_description'].custom_widget.height = 3
    form_fields['contactpage_keywords'].custom_widget = Text2ListWidget
    form_fields['event_title'].custom_widget = TextWidget
    form_fields['event_description'].custom_widget = TextAreaWidget
    form_fields['event_description'].custom_widget.height = 3
    form_fields['event_keywords'].custom_widget = Text2ListWidget
    form_fields['file_title'].custom_widget = TextWidget
    form_fields['file_description'].custom_widget = TextAreaWidget
    form_fields['file_description'].custom_widget.height = 3
    form_fields['file_keywords'].custom_widget = Text2ListWidget
    form_fields['folder_title'].custom_widget = TextWidget
    form_fields['folder_description'].custom_widget = TextAreaWidget
    form_fields['folder_description'].custom_widget.height = 3
    form_fields['folder_keywords'].custom_widget = Text2ListWidget
    form_fields['image_title'].custom_widget = TextWidget
    form_fields['image_description'].custom_widget = TextAreaWidget
    form_fields['image_description'].custom_widget.height = 3
    form_fields['image_keywords'].custom_widget = Text2ListWidget
    form_fields['link_title'].custom_widget = TextWidget
    form_fields['link_description'].custom_widget = TextAreaWidget
    form_fields['link_description'].custom_widget.height = 3
    form_fields['link_keywords'].custom_widget = Text2ListWidget
    form_fields['newsItem_title'].custom_widget = TextWidget
    form_fields['newsItem_description'].custom_widget = TextAreaWidget
    form_fields['newsItem_description'].custom_widget.height = 3
    form_fields['newsItem_keywords'].custom_widget = Text2ListWidget
    form_fields['topic_title'].custom_widget = TextWidget
    form_fields['topic_description'].custom_widget = TextAreaWidget
    form_fields['topic_description'].custom_widget.height = 3
    form_fields['topic_keywords'].custom_widget = Text2ListWidget
#    form_fields['robots_noodp'].custom_widget = CheckBoxWidget
#    form_fields['robots_noydir'].custom_widget = CheckBoxWidget
#    form_fields['robots_noarchive'].custom_widget = CheckBoxWidget
#    form_fields['robots_nosnippet'].custom_widget = CheckBoxWidget
#    form_fields['indexing_searchpage'].custom_widget = CheckBoxWidget
#    form_fields['indexing_loginregistrationpage'].custom_widget = CheckBoxWidget
#    form_fields['indexing_administrationpage'].custom_widget = CheckBoxWidget
#    form_fields['indexing_page'].custom_widget = CheckBoxWidget
#    form_fields['indexing_event'].custom_widget = CheckBoxWidget
#    form_fields['indexing_file'].custom_widget = CheckBoxWidget
#    form_fields['indexing_folder'].custom_widget = CheckBoxWidget
#    form_fields['indexing_image'].custom_widget = CheckBoxWidget  
#    form_fields['indexing_link'].custom_widget = CheckBoxWidget
#    form_fields['indexing_newsItem'].custom_widget = CheckBoxWidget
#    form_fields['indexing_topic'].custom_widget = CheckBoxWidget
    form_fields['tracking_code_header'].custom_widget = TextAreaWidget
    form_fields['tracking_code_header'].custom_widget.height = 6
    form_fields['tracking_code_footer'].custom_widget = TextAreaWidget
    form_fields['tracking_code_footer'].custom_widget.height = 6
    form_fields['not_displayed_types'].custom_widget = MultiCheckBoxThreeColumnWidget

    label = _("Plone SEO Configuration")
    description = _("seo_configlet_description", default="You can select what "
                    "content types are qSEOptimizer-enabled, and control if "
                    "Dublin Core metatags are exposed in the header of content "
                    "pages.")
    form_name = _("")
