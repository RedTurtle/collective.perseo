import re

from zope.interface import Interface
from zope.schema import TextLine, Text, List, Bool, Tuple, Choice
from zope.app.form.browser import TextAreaWidget, TextWidget  # ,CheckBoxWidget
from plone.fieldsets.fieldsets import FormFieldsets

from collective.perseo import perseoMessageFactory as _


class ISEOConfigWMToolsSchema(Interface):
    """Schema for WebMaster Tools"""

    googleWebmasterTools = TextLine(
        title=_("label_googleWebmasterTools", default=u"Google Webmaster Tools"),
        description=_("help__googleWebmasterTools", default=u"Enter an id for Google. https://www.google.com/webmasters/tools/"),
        required=False)

    yahooSiteExplorer = TextLine(
        title=_("label_yahooSiteExplorer", default=u"Yahoo Site Explorer"),
        description=_("help_yahooSiteExplorer", default=u"Enter an id for Yahoo. https://siteexplorer.search.yahoo.com/mysites"),
        required=False)

    bingWebmasterTools = TextLine(
        title=_("label_bingWebmasterTools", default=u"Bing Webmaster Tools"),
        description=_("help_bingWebmasterTools", default=u"Enter an id for Bing. http://www.bing.com/webmaster/"),
        required=False)

    tracking_code_header = Text(
        title=_("label_tracking_code_header", default=u"Tracking Code Header"),
        required=False)

    tracking_code_footer = Text(
        title=_("label_tracking_code_footer", default=u"Tracking Code Footer"),
        required=False)


class ISEOConfigTitleSchema_homepage(Interface):
    """Schema for Title homepage"""

    homepage_title = TextLine(
        title=_("label_homepage_title", default=u"Home Page Title"),
        required=False)

    homepage_description = Text(
        title=_("label_homepage_description", default=u"Home Page Description"),
        required=False)

    homepage_keywords = List(
        title=_("label_homepage_keywords", default=u"Home Page Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_document(Interface):
    """Schema for Title document"""

    document_title = TextLine(
        title=_("label_document_title", default=u"Single Page Title"),
        required=False)

    document_description = Text(
        title=_("label_document_description", default=u"Single Page Description"),
        required=False)

    document_keywords = List(
        title=_("label_document_keywords", default=u"Single Page Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_searchpage(Interface):
    """Schema for Title searchpage"""

    searchpage_title = TextLine(
        title=_("label_searchpage_title", default=u"Search Page Title"),
        required=False)

    searchpage_description = Text(
        title=_("label_searchpage_description", default=u"Search Page Description"),
        required=False)

    searchpage_keywords = List(
        title=_("label_searchpage_keywords", default=u"Search Page Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_notfoundpage(Interface):
    """Schema for Title notfoundpage"""

    notfoundpage_title = TextLine(
        title=_("label_notfoundpage_title", default=u"Not Found Page Title"),
        required=False)

    notfoundpage_description = Text(
        title=_("label_notfoundpage_description", default=u"Not Found Page Description"),
        required=False)

    notfoundpage_keywords = List(
        title=_("label_notfoundpage_keywords", default=u"Not Found Page Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_authorpage(Interface):
    """Schema for Title authorpage"""

    authorpage_title = TextLine(
        title=_("label_authorpage_title", default=u"Author Page Title"),
        required=False)

    authorpage_description = Text(
        title=_("label_authorpage_description", default=u"Author Page Description"),
        required=False)

    authorpage_keywords = List(
        title=_("label_authorpage_keywords", default=u"Author Page Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_sitemappage(Interface):
    """Schema for Title sitemappage"""

    sitemappage_title = TextLine(
        title=_("label_sitemappage_title", default=u"Site map Title"),
        required=False)

    sitemappage_description = Text(
        title=_("label_sitemappage_description", default=u"Site map Description"),
        required=False)

    sitemappage_keywords = List(
        title=_("label_sitemappage_keywords", default=u"Site map Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_accessibilitypage(Interface):
    """Schema for Title accessibilitypages"""

    accessibilitypage_title = TextLine(
        title=_("label_accessibilitypage_title", default=u"Accessibility Title"),
        required=False)

    accessibilitypage_description = Text(
        title=_("label_accessibilitypage_description", default=u"Accessibility Description"),
        required=False)

    accessibilitypage_keywords = List(
        title=_("label_accessibilitypage_keywords", default=u"Accessibility Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_contactpage(Interface):
    """Schema for Title contactpage"""

    contactpage_title = TextLine(
        title=_("label_contactpage_title", default=u"Contact Title"),
        required=False)

    contactpage_description = Text(
        title=_("label_contactpage_description", default=u"Contact Description"),
        required=False)

    contactpage_keywords = List(
        title=_("label_contactpage_keywords", default=u"Contact Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_event(Interface):
    """Schema for Title event"""

    event_title = TextLine(
        title=_("label_event_title", default=u"Event Title"),
        required=False)

    event_description = Text(
        title=_("label_event_description", default=u"Event Description"),
        required=False)

    event_keywords = List(
        title=_("label_event_keywords", default=u"Event Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_file(Interface):
    """Schema for Title file"""

    file_title = TextLine(
        title=_("label_file_title", default=u"File Title"),
        required=False)

    file_description = Text(
        title=_("label_file_description", default=u"File Description"),
        required=False)

    file_keywords = List(
        title=_("label_file_keywords", default=u"File Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_folder(Interface):
    """Schema for Title folder"""

    folder_title = TextLine(
        title=_("label_folder_title", default=u"Folder Title"),
        required=False)

    folder_description = Text(
        title=_("label_folder_description", default=u"Folder Description"),
        required=False)

    folder_keywords = List(
        title=_("label_folder_keywords", default=u"Folder Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_image(Interface):
    """Schema for Title image"""

    image_title = TextLine(
        title=_("label_image_title", default=u"Image Title"),
        required=False)

    image_description = Text(
        title=_("label_image_description", default=u"Image Description"),
        required=False)

    image_keywords = List(
        title=_("label_image_keywords", default=u"Image Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_link(Interface):
    """Schema for Title link"""

    link_title = TextLine(
        title=_("label_link_title", default=u"Link Title"),
        required=False)

    link_description = Text(
        title=_("label_link_description", default=u"Link Description"),
        required=False)

    link_keywords = List(
        title=_("label_link_keywords", default=u"Link Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_newsitem(Interface):
    """Schema for Title newsitem"""

    newsitem_title = TextLine(
        title=_("label_newsitem_title", default=u"NewsItem Title"),
        required=False)

    newsitem_description = Text(
        title=_("label_newsitem_description", default=u"NewsItem Description"),
        required=False)

    newsitem_keywords = List(
        title=_("label_newsitem_keywords", default=u"NewsItem Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema_topic(Interface):
    """Schema for Title topic"""

    topic_title = TextLine(
        title=_("label_topic_title", default=u"Topic Title"),
        required=False)

    topic_description = Text(
        title=_("label_topic_description", default=u"Topic Description"),
        required=False)

    topic_keywords = List(
        title=_("label_topic_keywords", default=u"Topic Keywords"),
        description=_("help_keywords", default=u"You can enter multiple keywords - one pr. line."),
        required=False)


class ISEOConfigTitleSchema(ISEOConfigTitleSchema_homepage,
                            ISEOConfigTitleSchema_document,
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
                            ISEOConfigTitleSchema_newsitem,
                            ISEOConfigTitleSchema_topic):
    """Schema for Title"""


class ISEOConfigIndexingSchema(Interface):
    """Schema for Indexing"""

    indexing_searchpage = Bool(
        title=_("label_search_page", default=u"Search pages"),
        default=False,
        required=False)

    indexing_loginregistrationpage = Bool(
        title=_("label_login_registration_page", default=u"Login and Registration pages"),
        default=False,
        required=False)

    indexing_administrationpage = Bool(
        title=_("label_administration_page", default=u"Administration pages"),
        default=False,
        required=False)

    indexing_page = Bool(
        title=_("label_single_pages", default=u"Single Pages"),
        default=False,
        required=False)

    indexing_event = Bool(
        title=_("label_indexing_event", default=u"Event"),
        default=False,
        required=False)

    indexing_file = Bool(
        title=_("label_indexing_file", default=u"File"),
        default=False,
        required=False)

    indexing_folder = Bool(
        title=_("label_indexing_folder", default=u"Folder"), default=False,
        required=False)

    indexing_image = Bool(
        title=_("label_indexing_image", default=u"Image"),
        default=False,
        required=False)

    indexing_link = Bool(
        title=_("label_indexing_link", default=u"Link"),
        default=False,
        required=False)

    indexing_newsitem = Bool(
        title=_("label_indexing_newsitem", default=u"NewsItem"),
        default=False,
        required=False)

    indexing_topic = Bool(
        title=_("label_indexing_topic", default=u"Topic"),
        default=False,
        required=False)

    robots_noodp = Bool(
        title=_("label_robots_noodp", default=u"Add noodp in whole site"),
        default=False,
        required=False)

    robots_noydir = Bool(
        title=_("label_robots_noydir", default=u"Add noydir in whole site"),
        default=False,
        required=False)

    robots_noarchive = Bool(
        title=_("label_robots_noarchive", default=u"Add noarchive in whole site"),
        default=False,
        required=False)

    robots_nosnippet = Bool(
        title=_("label_robots_nosnippet", default=u"Add nosnippet in whole site"),
        default=False,
        required=False)


class ISEOConfigSiteMapXMLSchema(Interface):
    """Schema for Site Map XML Tools"""

    not_included_types = Tuple(
        title=_("label_included_types", default=u"Types of content included in the XML Site Map"),
        description=_("help_included_types", default=u"The content types that should be included in the sitemap.xml.gz."),
        required=False,
        missing_value=tuple(),
        value_type=Choice(vocabulary="collective.perseo.vocabularies.ReallyUserFriendlyTypes"))

    ping_google = Bool(
        title=_("label_ping_google", default=u"Ping Google"),
        description=_("help_ping", default=u"Ping site automatically when the Site Map is updated."),
        default=False,
        required=False)

    ping_bing = Bool(
        title=_("label_ping_bing", default=u"Ping Bing"),
        description=_("help_ping", default=u"Ping site automatically when the Site Map is updated."),
        default=False,
        required=False)

    ping_ask = Bool(
        title=_("label_ping_ask", default=u"Ping Ask"),
        description=_("help_ping", default=u"Ping site automatically when the Site Map is updated."),
        default=False,
        required=False)


class ISEOConfigSchemaOrgSchema(Interface):
    """Schema for Schema.org"""

    itemscope_itemtype_attrs_enable = Bool(
        title=_("label_itemscope_itemtype_attrs_enable", default=u"Add itemscope and itemtype attributes to body tag"),
        default=False,
        required=False)


class ISEOConfigRSSSchema(Interface):
    """Schema for RSS"""

    indexing_feed_rss = Bool(
        title=_("label_indexing_feed_rss", default=u"Don't index RSS feeds"),
        default=False,
        required=False)


class ISEOSocialSchema(Interface):
    """Schema for social integrations"""

    twitter_site_id = Text(
        title=_("label_twitter_site_id", default=u"This site twitter ID"),
        required=False)


class ISEOConfigSchema(ISEOConfigWMToolsSchema,
                       ISEOConfigTitleSchema,
                       ISEOConfigIndexingSchema,
                       ISEOConfigSiteMapXMLSchema,
                       ISEOConfigSchemaOrgSchema,
                       ISEOConfigRSSSchema,
                       ISEOSocialSchema):
    """Combined schema for the adapter lookup.
    """

# Fieldset configurations

wmtoolsset = FormFieldsets(ISEOConfigWMToolsSchema)
wmtoolsset.id = 'seowmtools'
wmtoolsset.label = _(u'label_seowmtools', default=u'WM Tools')

titleset_homepage = FormFieldsets(ISEOConfigTitleSchema_homepage)
titleset_homepage.id = 'seotitle_homepage'
titleset_homepage.label = _(u'label_seotitle_homepage', default=u'Home Page')

titleset_document = FormFieldsets(ISEOConfigTitleSchema_document)
titleset_document.id = 'seotitle_document'
titleset_document.label = _(u'label_seotitle_document', default=u'Single Pages')

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

titleset_newsitem = FormFieldsets(ISEOConfigTitleSchema_newsitem)
titleset_newsitem.id = 'seotitle_newsitem'
titleset_newsitem.label = _(u'label_seotitle_newsitem', default=u'News Item')

titleset_topic = FormFieldsets(ISEOConfigTitleSchema_topic)
titleset_topic.id = 'seotitle_topic'
titleset_topic.label = _(u'label_seotitle_topic', default=u'Topic')

titleset = FormFieldsets(titleset_homepage, titleset_document, titleset_searchpage,
                         titleset_notfoundpage, titleset_authorpage, titleset_sitemappage,
                         titleset_accessibilitypage, titleset_contactpage, titleset_event,
                         titleset_file, titleset_folder, titleset_image, titleset_link,
                         titleset_newsitem, titleset_topic)
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

socialset = FormFieldsets(ISEOSocialSchema)
socialset.id = 'seosocial'
socialset.label = _(u'label_seosocial', default=u'Social')

class CodeTextAreaWidget(TextAreaWidget):
    height = 6


class TitleTextAreaWidget(TextWidget):
    displayWidth = 50


class DescTextAreaWidget(TextAreaWidget):
    height = 3


class Text2ListWidget(TextAreaWidget):
    height = 5
    splitter = re.compile(u'\\r?\\n', re.S | re.U)

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
