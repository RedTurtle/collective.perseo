from zope.interface import implements
from zope.component import adapts
from zope.app.component.hooks import getSite

from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.controlpanel.form import ControlPanelForm
from plone.app.controlpanel.widgets import MultiCheckBoxThreeColumnWidget

from Products.CMFDefault.formlib.schema import SchemaAdapterBase, ProxyFieldProperty
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName, safe_unicode
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.perseo import perseoMessageFactory as _
from collective.perseo.vocabulary import BAD_TYPES
from collective.perseo.browser.seo_schema import ISEOConfigSchema, wmtoolsset, socialset,\
    titleset, indexingset, sitemapxmlset, rssset, CodeTextAreaWidget,\
    TitleTextAreaWidget, DescTextAreaWidget, Text2ListWidget, TextWidget


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
    document_title = ProxyFieldProperty(ISEOConfigSchema['document_title'])
    document_description = ProxyFieldProperty(ISEOConfigSchema['document_description'])
    document_keywords = ProxyFieldProperty(ISEOConfigSchema['document_keywords'])
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
    newsitem_title = ProxyFieldProperty(ISEOConfigSchema['newsitem_title'])
    newsitem_description = ProxyFieldProperty(ISEOConfigSchema['newsitem_description'])
    newsitem_keywords = ProxyFieldProperty(ISEOConfigSchema['newsitem_keywords'])
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
    indexing_newsitem = ProxyFieldProperty(ISEOConfigSchema['indexing_newsitem'])
    indexing_topic = ProxyFieldProperty(ISEOConfigSchema['indexing_topic'])

    twitter_site_id = ProxyFieldProperty(ISEOConfigSchema['twitter_site_id'])

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


class PerSEOConfig(ControlPanelForm):

    template = ViewPageTemplateFile('templates/seo-control-panel.pt')

    form_fields = FormFieldsets(wmtoolsset, titleset, indexingset, sitemapxmlset, rssset, socialset)
    form_fields['twitter_site_id'].custom_widget = TextWidget
    form_fields['googleWebmasterTools'].custom_widget = TextWidget
    form_fields['yahooSiteExplorer'].custom_widget = TextWidget
    form_fields['bingWebmasterTools'].custom_widget = TextWidget
    form_fields['homepage_title'].custom_widget = TitleTextAreaWidget
    form_fields['homepage_description'].custom_widget = DescTextAreaWidget
    form_fields['homepage_keywords'].custom_widget = Text2ListWidget
    form_fields['document_title'].custom_widget = TitleTextAreaWidget
    form_fields['document_description'].custom_widget = DescTextAreaWidget
    form_fields['document_keywords'].custom_widget = Text2ListWidget
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
    form_fields['newsitem_title'].custom_widget = TitleTextAreaWidget
    form_fields['newsitem_description'].custom_widget = DescTextAreaWidget
    form_fields['newsitem_keywords'].custom_widget = Text2ListWidget
    form_fields['topic_title'].custom_widget = TitleTextAreaWidget
    form_fields['topic_description'].custom_widget = DescTextAreaWidget
    form_fields['topic_keywords'].custom_widget = Text2ListWidget
    form_fields['tracking_code_header'].custom_widget = CodeTextAreaWidget
    form_fields['tracking_code_footer'].custom_widget = CodeTextAreaWidget
    form_fields['not_included_types'].custom_widget = MultiCheckBoxThreeColumnWidget

    label = _("PerSEO Configuration")
    description = _("")
    form_name = _("")
