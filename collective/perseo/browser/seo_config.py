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
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.perseo import perseoMessageFactory as _
from collective.perseo.browser.types import BAD_TYPES

class ISEOConfigWMToolsSchema(Interface):
    """Schema for WebMaster Tools"""
    
    googleWebmasterTools = TextLine(
        title=_("label_googleWebmasterTools",
                default=u"Google Webmaster Tools"),
        description=_("help__googleWebmasterTools",
                      default=u"Enter an id for Google. https://www.google.com/webmasters/tools/"),
        required=False)
    
    yahooSiteExplorer = TextLine(
        title=_("label_yahooSiteExplorer",
                default=u"Yahoo Site Explorer"),
        description=_("help_yahooSiteExplorer",
                      default=u"Enter an id for Yahoo. https://siteexplorer.search.yahoo.com/mysites"),
        required=False)
    
    bingWebmasterTools = TextLine(
        title=_("label_bingWebmasterTools",
                default=u"Bing Webmaster Tools"),
        description=_("help_bingWebmasterTools",
                      default=u"Enter an id for Bing. http://www.bing.com/webmaster/"),
        required=False)
    
    tracking_code_header = Text(
        title=_("label_tracking_code_header",
                default=u"Tracking Code Header"),
        required=False)
    
    tracking_code_footer = Text(
        title=_("label_tracking_code_footer",
                default=u"Tracking Code Footer"),
        required=False)

class ISEOConfigTitleSchema_homepage(Interface):
    """Schema for Title homepage"""
    
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_singlepage(Interface):
    """Schema for Title singlepage"""
  
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_searchpage(Interface):
    """Schema for Title searchpage"""
        
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_notfoundpage(Interface):
    """Schema for Title notfoundpage"""
        
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_authorpage(Interface):
    """Schema for Title authorpage"""
        
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_sitemappage(Interface):
    """Schema for Title sitemappage"""
        
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_accessibilitypage(Interface):
    """Schema for Title accessibilitypages"""
    
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_contactpage(Interface):
    """Schema for Title contactpage"""
    
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_event(Interface):
    """Schema for Title event"""
    
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_file(Interface):
    """Schema for Title file"""
    
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_folder(Interface):
    """Schema for Title folder"""
   
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_image(Interface):
    """Schema for Title image"""
        
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_link(Interface):
    """Schema for Title link"""
       
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_newsItem(Interface):
    """Schema for Title newsItem"""
       
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)

class ISEOConfigTitleSchema_topic(Interface):
    """Schema for Title topic"""
  
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
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        required=False)
    
class ISEOConfigTitleSchema(ISEOConfigTitleSchema_homepage,
                            ISEOConfigTitleSchema_singlepage,
                            ISEOConfigTitleSchema_searchpage,
                            ISEOConfigTitleSchema_notfoundpage,
                            ISEOConfigTitleSchema_authorpage,
                            ISEOConfigTitleSchema_sitemappage,
                            ISEOConfigTitleSchema_accessibilitypage,
                            ISEOConfigTitleSchema_contactpage,
                            ISEOConfigTitleSchema_event,
                            ISEOConfigTitleSchema_file,
                            ISEOConfigTitleSchema_folder,
                            ISEOConfigTitleSchema_image,
                            ISEOConfigTitleSchema_link,
                            ISEOConfigTitleSchema_newsItem,
                            ISEOConfigTitleSchema_topic):
    """Schema for Title"""
    
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
    
    not_included_types = Tuple(
        title=_("label_included_types",
                default=u"Types of content included in the XML Site Map"),
        description=_("help_included_types",
                      default=u"The content types that should be included in the sitemap.xml.gz."),
        required=False,
        missing_value=tuple(),
        value_type=Choice(
            vocabulary="collective.perseo.vocabularies.ReallyUserFriendlyTypes")
        )
    
    ping_google = Bool(
        title=_("label_ping_google",
                default=u"Ping Google"),
        description=_("help_ping",
                      default=u"Ping site automatically when the Site Map is updated."),
        default=False,
        required=False)
    
    ping_bing = Bool(
        title=_("label_ping_bing",
                default=u"Ping Bing"),
        description=_("help_ping",
                      default=u"Ping site automatically when the Site Map is updated."),
        default=False,
        required=False)
    
    ping_ask = Bool(
        title=_("label_ping_ask",
                default=u"Ping Ask"),
        description=_("help_ping",
                      default=u"Ping site automatically when the Site Map is updated."),
        default=False,
        required=False)

class ISEOConfigSchemaOrgSchema(Interface):
    """Schema for Schema.org"""
    
    itemscope_itemtype_attrs_enable = Bool(
        title=_("label_itemscope_itemtype_attrs_enable",
                default=u"Add itemscope and itemtype attributes to body tag"),
        default=False,
        required=False)
    
class ISEOConfigRSSSchema(Interface):
    """Schema for RSS"""
    
    indexing_feed_rss = Bool(
        title=_("label_indexing_feed_rss",
                default=u"Don't index RSS feeds"),
        default=False,
        required=False)

class ISEOConfigSchema(ISEOConfigWMToolsSchema,
                       ISEOConfigTitleSchema,
                       ISEOConfigIndexingSchema,
                       ISEOConfigSiteMapXMLSchema,
                       ISEOConfigSchemaOrgSchema,
                       ISEOConfigRSSSchema):
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
    
    def getIncludedTypes(self):
        not_included_types = getattr(self.context, 'not_included_types', ())
        
        return [t for t in self.portal_types.listContentTypes()
                        if t not in not_included_types and
                           t not in BAD_TYPES]

    def setNotIncludedTypes(self, value):
        # The menu pretends to be a whitelist, but we are storing a blacklist so that
        # new types are searchable by default. Inverse the list.
        allTypes = self.portal_types.listContentTypes()

        blacklistedTypes = [t for t in allTypes if t not in value
                                                and t not in BAD_TYPES]
        self.context.not_included_types = blacklistedTypes

    not_included_types = property(getIncludedTypes, setNotIncludedTypes)
    itemscope_itemtype_attrs_enable = ProxyFieldProperty(ISEOConfigSchema['itemscope_itemtype_attrs_enable'])
    indexing_feed_rss = ProxyFieldProperty(ISEOConfigSchema['indexing_feed_rss'])
    ping_google = ProxyFieldProperty(ISEOConfigSchema['ping_google'])
    ping_bing = ProxyFieldProperty(ISEOConfigSchema['ping_bing'])
    ping_ask = ProxyFieldProperty(ISEOConfigSchema['ping_ask'])

# Fieldset configurations

wmtoolsset = FormFieldsets(ISEOConfigWMToolsSchema)
wmtoolsset.id = 'seowmtools'
wmtoolsset.label = _(u'label_seowmtools', default=u'WM Tools')

titleset_homepage = FormFieldsets(ISEOConfigTitleSchema_homepage)
titleset_homepage.id = 'seotitle_homepage'
titleset_homepage.label = _(u'label_seotitle_homepage', default=u'Home Page')

titleset_singlepage = FormFieldsets(ISEOConfigTitleSchema_singlepage)
titleset_singlepage.id = 'seotitle_singlepage'
titleset_singlepage.label = _(u'label_seotitle_singlepage', default=u'Single Pages')

titleset_searchpage = FormFieldsets(ISEOConfigTitleSchema_searchpage)
titleset_searchpage.id = 'seotitle_searchpage'
titleset_searchpage.label = _(u'label_seotitle_searchpage', default=u'Search Page')

titleset_notfoundpage = FormFieldsets(ISEOConfigTitleSchema_notfoundpage)
titleset_notfoundpage.id = 'seotitle_notfoundpage'
titleset_notfoundpage.label = _(u'label_seotitle_notfoundpage', default=u'Not Found Page')

titleset_authorpage = FormFieldsets(ISEOConfigTitleSchema_authorpage)
titleset_authorpage.id = 'seotitle_authorpage'
titleset_authorpage.label = _(u'label_seotitle_authorpage', default=u'Author Page')

titleset_sitemappage = FormFieldsets(ISEOConfigTitleSchema_sitemappage)
titleset_sitemappage.id = 'seotitle_sitemappage'
titleset_sitemappage.label = _(u'label_seotitle_sitemappage', default=u'Site Map')

titleset_accessibilitypage = FormFieldsets(ISEOConfigTitleSchema_accessibilitypage)
titleset_accessibilitypage.id = 'seotitle_accessibilitypage'
titleset_accessibilitypage.label = _(u'label_seotitle_accessibilitypage', default=u'Accessibility')

titleset_contactpage = FormFieldsets(ISEOConfigTitleSchema_contactpage)
titleset_contactpage.id = 'seotitle_contactpage'
titleset_contactpage.label = _(u'label_seotitle_contactpage', default=u'Contact')

titleset_event = FormFieldsets(ISEOConfigTitleSchema_event)
titleset_event.id = 'seotitle_event'
titleset_event.label = _(u'label_seotitle_event', default=u'Event')

titleset_file = FormFieldsets(ISEOConfigTitleSchema_file)
titleset_file.id = 'seotitle_file'
titleset_file.label = _(u'label_seotitle_file', default=u'File')

titleset_folder = FormFieldsets(ISEOConfigTitleSchema_folder)
titleset_folder.id = 'seotitle_folder'
titleset_folder.label = _(u'label_seotitle_folder', default=u'Folder')

titleset_image = FormFieldsets(ISEOConfigTitleSchema_image)
titleset_image.id = 'seotitle_image'
titleset_image.label = _(u'label_seotitle_image', default=u'Image')

titleset_link = FormFieldsets(ISEOConfigTitleSchema_link)
titleset_link.id = 'seotitle_link'
titleset_link.label = _(u'label_seotitle_link', default=u'Link')

titleset_newsItem = FormFieldsets(ISEOConfigTitleSchema_newsItem)
titleset_newsItem.id = 'seotitle_newsItem'
titleset_newsItem.label = _(u'label_seotitle_newsItem', default=u'News Item')

titleset_topic = FormFieldsets(ISEOConfigTitleSchema_topic)
titleset_topic.id = 'seotitle_topic'
titleset_topic.label = _(u'label_seotitle_topic', default=u'Topic')

titleset = FormFieldsets(titleset_homepage, titleset_singlepage, titleset_searchpage,
                         titleset_notfoundpage, titleset_authorpage, titleset_sitemappage,
                         titleset_accessibilitypage, titleset_contactpage, titleset_event,
                         titleset_file, titleset_folder, titleset_image, titleset_link,
                         titleset_newsItem, titleset_topic)
titleset.id = 'seotitle'
titleset.label = _(u'label_seotitle', default=u'Title')

indexingset = FormFieldsets(ISEOConfigIndexingSchema)
indexingset.id = 'seoindexing'
indexingset.label = _(u'label_seoindexing', default=u'Indexing')
indexingset.description = _(u'description_seoindexing', default=u"By selecting the options below" \
                                " you decide to disable the indexing of resources using noindex and nofollow")

sitemapxmlset = FormFieldsets(ISEOConfigSiteMapXMLSchema)
sitemapxmlset.id = 'seositemapxml'
sitemapxmlset.label = _(u'label_seositemapxml', default=u'Site Map')

schemaorgset = FormFieldsets(ISEOConfigSchemaOrgSchema)
schemaorgset.id = 'seoschemaorg'
schemaorgset.label = _(u'label_seoschemaorg', default=u'Schema.org')

rssset = FormFieldsets(ISEOConfigRSSSchema)
rssset.id = 'seorss'
rssset.label = _(u'label_seorss', default=u'RSS')

class CodeTextAreaWidget(TextAreaWidget):
    height = 6
    
class TitleTextAreaWidget(TextWidget):
    displayWidth = 50

class DescTextAreaWidget(TextAreaWidget):
    height = 3

class Text2ListWidget(TextAreaWidget):
    height = 5
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
    
    template = ViewPageTemplateFile('templates/seo-control-panel.pt')
    
    form_fields = FormFieldsets(wmtoolsset, titleset, indexingset, sitemapxmlset, rssset)
    
    form_fields['googleWebmasterTools'].custom_widget = TextWidget
    form_fields['yahooSiteExplorer'].custom_widget = TextWidget
    form_fields['bingWebmasterTools'].custom_widget = TextWidget
    form_fields['homepage_title'].custom_widget = TitleTextAreaWidget
    form_fields['homepage_description'].custom_widget = DescTextAreaWidget
    form_fields['homepage_keywords'].custom_widget = Text2ListWidget
    form_fields['singlepage_title'].custom_widget = TitleTextAreaWidget
    form_fields['singlepage_description'].custom_widget = DescTextAreaWidget
    form_fields['singlepage_keywords'].custom_widget = Text2ListWidget
    form_fields['searchpage_title'].custom_widget = TitleTextAreaWidget
    form_fields['searchpage_description'].custom_widget = DescTextAreaWidget
    form_fields['searchpage_keywords'].custom_widget = Text2ListWidget
    form_fields['notfoundpage_title'].custom_widget = TitleTextAreaWidget
    form_fields['notfoundpage_description'].custom_widget = DescTextAreaWidget
    form_fields['notfoundpage_keywords'].custom_widget = Text2ListWidget
    form_fields['authorpage_title'].custom_widget = TitleTextAreaWidget
    form_fields['authorpage_description'].custom_widget = DescTextAreaWidget
    form_fields['authorpage_keywords'].custom_widget = Text2ListWidget
    form_fields['sitemappage_title'].custom_widget = TitleTextAreaWidget
    form_fields['sitemappage_description'].custom_widget = DescTextAreaWidget
    form_fields['sitemappage_keywords'].custom_widget = Text2ListWidget
    form_fields['accessibilitypage_title'].custom_widget = TitleTextAreaWidget
    form_fields['accessibilitypage_description'].custom_widget = DescTextAreaWidget
    form_fields['accessibilitypage_keywords'].custom_widget = Text2ListWidget
    form_fields['contactpage_title'].custom_widget = TitleTextAreaWidget
    form_fields['contactpage_description'].custom_widget = DescTextAreaWidget
    form_fields['contactpage_keywords'].custom_widget = Text2ListWidget
    form_fields['event_title'].custom_widget = TitleTextAreaWidget
    form_fields['event_description'].custom_widget = DescTextAreaWidget
    form_fields['event_keywords'].custom_widget = Text2ListWidget
    form_fields['file_title'].custom_widget = TitleTextAreaWidget
    form_fields['file_description'].custom_widget = DescTextAreaWidget
    form_fields['file_keywords'].custom_widget = Text2ListWidget
    form_fields['folder_title'].custom_widget = TitleTextAreaWidget
    form_fields['folder_description'].custom_widget = DescTextAreaWidget
    form_fields['folder_keywords'].custom_widget = Text2ListWidget
    form_fields['image_title'].custom_widget = TitleTextAreaWidget
    form_fields['image_description'].custom_widget = DescTextAreaWidget
    form_fields['image_keywords'].custom_widget = Text2ListWidget
    form_fields['link_title'].custom_widget = TitleTextAreaWidget
    form_fields['link_description'].custom_widget = DescTextAreaWidget
    form_fields['link_keywords'].custom_widget = Text2ListWidget
    form_fields['newsItem_title'].custom_widget = TitleTextAreaWidget
    form_fields['newsItem_description'].custom_widget = DescTextAreaWidget
    form_fields['newsItem_keywords'].custom_widget = Text2ListWidget
    form_fields['topic_title'].custom_widget = TitleTextAreaWidget
    form_fields['topic_description'].custom_widget = DescTextAreaWidget
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
    form_fields['tracking_code_header'].custom_widget = CodeTextAreaWidget
    form_fields['tracking_code_footer'].custom_widget = CodeTextAreaWidget
    form_fields['not_included_types'].custom_widget = MultiCheckBoxThreeColumnWidget
#    form_fields['itemscope_itemtype_attrs_enable'].custom_widget = CheckBoxWidget
#    form_fields['indexing_feed_rss'].custom_widget = CheckBoxWidget

#    form_fields['ping_google'].custom_widget = CheckBoxWidget
#    form_fields['ping_bing'].custom_widget = CheckBoxWidget
#    form_fields['ping_ask'].custom_widget = CheckBoxWidget
    
    label = _("PerSEO Configuration")
    description = _("")
    form_name = _("")
