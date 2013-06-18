from zope.interface import Interface
from zope import schema
from collective.perseo import perseoMessageFactory as _
from collective.perseo.interfaces.metaconfig import ISEOConfigTitleSchema


TYPE_CONFIGURATION = ('search_page', 'login_registration_page', 'administration_page',
                      'document', 'event', 'file', 'folder', 'image', 'link',
                      'newsitem', 'topic')


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

    og_site_name = schema.TextLine(
        title=_("label_og_site_name",
                default=u"Site name for Social Networks"),
        description=_("help_og_site_name",
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


def add_fields_to_indexing_schema(schemata):
    for t in TYPE_CONFIGURATION:
        title = ' '.join(t.split('_'))

        meta_robots_index_override = schema.Bool(
            title=_("label_meta_robots_override_%s" % t,
                    default=u"Override the default for %s" % title),
            default=False,
            required=False)
        meta_robots_index_override.__name__ = 'meta_robots_index_override_%s' % t
        meta_robots_index_override.interface = schemata
        schemata._InterfaceClass__attrs[meta_robots_index_override.__name__] = meta_robots_index_override

        meta_robots_follow = schema.Choice(
            title=_("label_meta_robots_follow_%s" % t,
                    default=u"Meta Robots Follow Tag for %s" % title),
            values=['follow', 'nofollow'],
            required=False)
        meta_robots_follow.__name__ = 'meta_robots_follow_%s' % t
        meta_robots_follow.interface = schemata
        schemata._InterfaceClass__attrs[meta_robots_follow.__name__] = meta_robots_follow

        meta_robots_index = schema.Choice(
            title=_("label_meta_robots_index_%s" % t,
                    default=u"Meta Robots Index Tag for %s" % title),
            values=['index', 'noindex'],
            required=False)
        meta_robots_index.__name__ = 'meta_robots_index_%s' % t
        meta_robots_index.interface = schemata
        schemata._InterfaceClass__attrs[meta_robots_index.__name__] = meta_robots_index

        meta_robots_advanced = schema.List(
            title=_("label_meta_robots_advanced_%s" % t,
                    default=u"Meta Robots Advanced Tag for %s" % title),
            value_type=schema.Choice(
                    values=['noodp', 'noydir', 'noarchive', 'nosnippet']
                    ),
            required=False)
        meta_robots_advanced.__name__ = 'meta_robots_advanced_%s' % t
        meta_robots_advanced.interface = schemata
        schemata._InterfaceClass__attrs[meta_robots_advanced.__name__] = meta_robots_advanced

add_fields_to_indexing_schema(ISEOConfigIndexingSchema)


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
