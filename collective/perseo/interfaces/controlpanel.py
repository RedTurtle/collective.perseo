from zope.interface import Interface
from zope import schema
from collective.perseo import perseoMessageFactory as _
from collective.perseo.interfaces.metaconfig import ISEOConfigTitleSchema


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

class ISEOConfigSocialSchema(Interface):
    """Schema for Social Networks"""

    site_name = schema.TextLine(
        title=_("label_social_site_name",
                default=u"Site name for Social Networks"),
        description=_("help_social_site_name",
                      default=u"Enter your site name"),
        required=False)

    facebook_admins = schema.TextLine(
        title=_("label_facebook_admins",
                default=u"Facebook admins IDs"),
        description=_("help_facebook_admins",
                      default=u"Enter a Facebook admins Ids"),
        required=False)

    twitter_site = schema.TextLine(
        title=_("label_twitter_site",
                default=u"Twitter site account"),
        description=_("help_twitter_site",
                      default=u"Enter twitter site account name, ie. @redturtle"),
        required=False)


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


class ISEOControlpanel(ISEOConfigWMToolsSchema,
                       ISEOConfigTitleSchema,
                       ISEOConfigIndexingSchema,
                       ISEOConfigSiteMapXMLSchema,
                       ISEOConfigSchemaOrgSchema,
                       ISEOConfigSocialSchema,
                       ISEOConfigRSSSchema):
    """Combined schema for the adapter lookup.
    """
