from zope.interface import Interface
from zope import schema
from collective.perseo import perseoMessageFactory as _


class ISEOConfigWMToolsSchema(Interface):
    """Schema for WebMaster Tools"""

    googleWebmasterTools = schema.TextLine(
        title=_("label_googleWebmasterTools",
                default=u"Google Webmaster Tools"),
        description=_("help__googleWebmasterTools",
                      default=u"Enter an id for Google. https://www.google.com/webmasters/tools/"),
        required=False)

    bingWebmasterTools = schema.TextLine(
        title=_("label_bingWebmasterTools",
                default=u"Bing Webmaster Tools"),
        description=_("help_bingWebmasterTools",
                      default=u"Enter an id for Bing. http://www.bing.com/webmaster/"),
        required=False)

    tracking_code_header = schema.Text(
        title=_("label_tracking_code_header",
                default=u"Tracking Code Header"),
        required=False)

    tracking_code_footer = schema.Text(
        title=_("label_tracking_code_footer",
                default=u"Tracking Code Footer"),
        required=False)

    google_publisher = schema.TextLine(
        title=_("label_google_publisher",
                default=u"Google+ Publisher Page"),
        description=_("help_google_publisher",
                      default=u"Enter a Google+ Page, ie. https://plus.google.com/117510669985299383051/"),
        required=False)


class ISEOConfigTitleSchema_homepage(Interface):
    """Schema for Title homepage"""

    homepage_title = schema.TextLine(
        title=_("label_homepage_title",
                default=u"Home Page Title"),
        required=False)

    homepage_description = schema.Text(
        title=_("label_homepage_description",
                default=u"Home Page Description"),
        required=False)

    homepage_keywords = schema.List(
        title=_("label_homepage_keywords",
                default=u"Home Page Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_searchpage(Interface):
    """Schema for Title searchpage"""

    searchpage_title = schema.TextLine(
        title=_("label_searchpage_title",
                default=u"Search Page Title"),
        required=False)

    searchpage_description = schema.Text(
        title=_("label_searchpage_description",
                default=u"Search Page Description"),
        required=False)

    searchpage_keywords = schema.List(
        title=_("label_searchpage_keywords",
                default=u"Search Page Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_notfoundpage(Interface):
    """Schema for Title notfoundpage"""

    notfoundpage_title = schema.TextLine(
        title=_("label_notfoundpage_title",
                default=u"Not Found Page Title"),
        required=False)

    notfoundpage_description = schema.Text(
        title=_("label_notfoundpage_description",
                default=u"Not Found Page Description"),
        required=False)

    notfoundpage_keywords = schema.List(
        title=_("label_notfoundpage_keywords",
                default=u"Not Found Page Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_authorpage(Interface):
    """Schema for Title authorpage"""

    authorpage_title = schema.TextLine(
        title=_("label_authorpage_title",
                default=u"Author Page Title"),
        required=False)

    authorpage_description = schema.Text(
        title=_("label_authorpage_description",
                default=u"Author Page Description"),
        required=False)

    authorpage_keywords = schema.List(
        title=_("label_authorpage_keywords",
                default=u"Author Page Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_sitemappage(Interface):
    """Schema for Title sitemappage"""

    sitemappage_title = schema.TextLine(
        title=_("label_sitemappage_title",
                default=u"Site map Title"),
        required=False)

    sitemappage_description = schema.Text(
        title=_("label_sitemappage_description",
                default=u"Site map Description"),
        required=False)

    sitemappage_keywords = schema.List(
        title=_("label_sitemappage_keywords",
                default=u"Site map Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_accessibilitypage(Interface):
    """Schema for Title accessibilitypages"""

    accessibilitypage_title = schema.TextLine(
        title=_("label_accessibilitypage_title",
                default=u"Accessibility Title"),
        required=False)

    accessibilitypage_description = schema.Text(
        title=_("label_accessibilitypage_description",
                default=u"Accessibility Description"),
        required=False)

    accessibilitypage_keywords = schema.List(
        title=_("label_accessibilitypage_keywords",
                default=u"Accessibility Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_contactpage(Interface):
    """Schema for Title contactpage"""

    contactpage_title = schema.TextLine(
        title=_("label_contactpage_title",
                default=u"Contact Title"),
        required=False)

    contactpage_description = schema.Text(
        title=_("label_contactpage_description",
                default=u"Contact Description"),
        required=False)

    contactpage_keywords = schema.List(
        title=_("label_contactpage_keywords",
                default=u"Contact Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_document(Interface):
    """Schema for Title document"""

    document_title = schema.TextLine(
        title=_("label_document_title",
                default=u"Single Page Title"),
        required=False)

    document_description = schema.Text(
        title=_("label_document_description",
                default=u"Single Page Description"),
        required=False)

    document_keywords = schema.List(
        title=_("label_document_keywords",
                default=u"Single Page Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_event(Interface):
    """Schema for Title event"""

    event_title = schema.TextLine(
        title=_("label_event_title",
                default=u"Event Title"),
        required=False)

    event_description = schema.Text(
        title=_("label_event_description",
                default=u"Event Description"),
        required=False)

    event_keywords = schema.List(
        title=_("label_event_keywords",
                default=u"Event Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_file(Interface):
    """Schema for Title file"""

    file_title = schema.TextLine(
        title=_("label_file_title",
                default=u"File Title"),
        required=False)

    file_description = schema.Text(
        title=_("label_file_description",
                default=u"File Description"),
        required=False)

    file_keywords = schema.List(
        title=_("label_file_keywords",
                default=u"File Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_folder(Interface):
    """Schema for Title folder"""

    folder_title = schema.TextLine(
        title=_("label_folder_title",
                default=u"Folder Title"),
        required=False)

    folder_description = schema.Text(
        title=_("label_folder_description",
                default=u"Folder Description"),
        required=False)

    folder_keywords = schema.List(
        title=_("label_folder_keywords",
                default=u"Folder Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_image(Interface):
    """Schema for Title image"""

    image_title = schema.TextLine(
        title=_("label_image_title",
                default=u"Image Title"),
        required=False)

    image_description = schema.Text(
        title=_("label_image_description",
                default=u"Image Description"),
        required=False)

    image_keywords = schema.List(
        title=_("label_image_keywords",
                default=u"Image Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_link(Interface):
    """Schema for Title link"""

    link_title = schema.TextLine(
        title=_("label_link_title",
                default=u"Link Title"),
        required=False)

    link_description = schema.Text(
        title=_("label_link_description",
                default=u"Link Description"),
        required=False)

    link_keywords = schema.List(
        title=_("label_link_keywords",
                default=u"Link Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_newsItem(Interface):
    """Schema for Title newsItem"""

    newsItem_title = schema.TextLine(
        title=_("label_newsItem_title",
                default=u"NewsItem Title"),
        required=False)

    newsItem_description = schema.Text(
        title=_("label_newsItem_description",
                default=u"NewsItem Description"),
        required=False)

    newsItem_keywords = schema.List(
        title=_("label_newsItem_keywords",
                default=u"NewsItem Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
        required=False)


class ISEOConfigTitleSchema_topic(Interface):
    """Schema for Title topic"""

    topic_title = schema.TextLine(
        title=_("label_topic_title",
                default=u"Topic Title"),
        required=False)

    topic_description = schema.Text(
        title=_("label_topic_description",
                default=u"Topic Description"),
        required=False)

    topic_keywords = schema.List(
        title=_("label_topic_keywords",
                default=u"Topic Keywords"),
        description=_("help_keywords",
                      default=u"You can enter multiple keywords - one pr. line."),
        value_type=schema.TextLine(),
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
                            ISEOConfigTitleSchema_newsItem,
                            ISEOConfigTitleSchema_topic):
    """Schema for Title"""


class ISEOConfigIndexingSchema(Interface):
    """Schema for Indexing"""

    indexing_searchpage = schema.Bool(
        title=_("label_search_page",
                default=u"Search pages"),
        default=False,
        required=False)

    indexing_loginregistrationpage = schema.Bool(
        title=_("label_login_registration_page",
                default=u"Login and Registration pages"),
        default=False,
        required=False)

    indexing_administrationpage = schema.Bool(
        title=_("label_administration_page",
                default=u"Administration pages"),
        default=False,
        required=False)

    indexing_page = schema.Bool(
        title=_("label_single_pages",
                default=u"Single Pages"),
        default=False,
        required=False)

    indexing_event = schema.Bool(
        title=_("label_indexing_event",
                default=u"Event"),
        default=False,
        required=False)

    indexing_file = schema.Bool(
        title=_("label_indexing_file",
                default=u"File"),
        default=False,
        required=False)

    indexing_folder = schema.Bool(
        title=_("label_indexing_folder",
                default=u"Folder"),
        default=False,
        required=False)

    indexing_image = schema.Bool(
        title=_("label_indexing_image",
                default=u"Image"),
        default=False,
        required=False)

    indexing_link = schema.Bool(
        title=_("label_indexing_link",
                default=u"Link"),
        default=False,
        required=False)

    indexing_newsItem = schema.Bool(
        title=_("label_indexing_newsItem",
                default=u"NewsItem"),
        default=False,
        required=False)

    indexing_topic = schema.Bool(
        title=_("label_indexing_topic",
                default=u"Topic"),
        default=False,
        required=False)

    robots_noodp = schema.Bool(
        title=_("label_robots_noodp",
                default=u"Add noodp in whole site"),
        default=False,
        required=False)

    robots_noydir = schema.Bool(
        title=_("label_robots_noydir",
                default=u"Add noydir in whole site"),
        default=False,
        required=False)

    robots_noarchive = schema.Bool(
        title=_("label_robots_noarchive",
                default=u"Add noarchive in whole site"),
        default=False,
        required=False)

    robots_nosnippet = schema.Bool(
        title=_("label_robots_nosnippet",
                default=u"Add nosnippet in whole site"),
        default=False,
        required=False)


class ISEOConfigSiteMapXMLSchema(Interface):
    """Schema for Site Map XML Tools"""

    not_included_types = schema.Tuple(
        title=_("label_included_types",
                default=u"Types of content included in the XML Site Map"),
        description=_("help_included_types",
                      default=u"The content types that should be included in the sitemap.xml.gz."),
        required=False,
        value_type=schema.Choice(
            vocabulary="collective.perseo.vocabularies.ReallyUserFriendlyTypes")
        )

    ping_google = schema.Bool(
        title=_("label_ping_google",
                default=u"Ping Google"),
        description=_("help_ping",
                      default=u"Ping site automatically when the Site Map is updated."),
        default=False,
        required=False)

    ping_bing = schema.Bool(
        title=_("label_ping_bing",
                default=u"Ping Bing"),
        description=_("help_ping",
                      default=u"Ping site automatically when the Site Map is updated."),
        default=False,
        required=False)

    ping_ask = schema.Bool(
        title=_("label_ping_ask",
                default=u"Ping Ask"),
        description=_("help_ping",
                      default=u"Ping site automatically when the Site Map is updated."),
        default=False,
        required=False)


class ISEOConfigSchemaOrgSchema(Interface):
    """Schema for Schema.org"""

    itemscope_itemtype_attrs_enable = schema.Bool(
        title=_("label_itemscope_itemtype_attrs_enable",
                default=u"Add itemscope and itemtype attributes to body tag"),
        default=False,
        required=False)


class ISEOConfigRSSSchema(Interface):
    """Schema for RSS"""

    indexing_feed_rss = schema.Bool(
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
