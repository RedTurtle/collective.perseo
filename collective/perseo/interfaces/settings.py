from zope.interface import Interface
from zope import schema
from collective.perseo import perseoMessageFactory as _


class ISEODefaultSettings(Interface):

    title = schema.TextLine(
        title=_("label_title",
                default=u"Title Tag"),
        description=_("help_title",
                      default=(u"Text to be present in TITLE tag. It is "
                          "displayed in browser title bar. Search engines "
                          "display it as a title of the document.")),
        required=False)

    title_override = schema.Bool(
        title=_("label_title_override",
                default=u"Override the default"),
        default=False,
        required=False)

    description = schema.Text(
        title=_("label_description",
                default=u"Meta Description Tag"),
        description=_("help_description",
                      default=(u"Description of the document to be indexed by "
                          "Search Engines. This text will be present in meta "
                          "description tag in page HTML source.")),
        required=False)

    description_override = schema.Bool(
        title=_("label_title_override",
                default=u"Override the default"),
        default=False,
        required=False)

    keywords = schema.List(
        title=_("label_keywords",
                default=u"Meta Keywords Tag"),
        description=_("help_keywords",
                      default=(u"Keywords, the page will be indexed with. "
                          "Enter each keyword in separate line, please. "
                          "Though the relevance of listing meta keywords is "
                          "of questionable value now, it is useful to set "
                          "meta keywords for pages - for future reference.")),
        value_type=schema.TextLine(),
        required=False)

    keywords_override = schema.Bool(
        title=_("label_title_override",
                default=u"Override the default"),
        default=False,
        required=False)


class ISEOAdvancedSettings(Interface):

    meta_robots_follow = schema.Choice(
        title=_("label_meta_robots_follow",
                default=u"Meta Robots Follow Tag"),
        values=['follow', 'nofollow'],
        required=False)

    meta_robots_follow_override = schema.Bool(
        title=_("label_title_override",
                default=u"Override the default"),
        default=False,
        required=False)

    meta_robots_index = schema.Choice(
        title=_("label_meta_robots_index",
                default=u"Meta Robots Index Tag"),
        values=['index', 'noindex'],
        required=False)

    meta_robots_index_override = schema.Bool(
        title=_("label_title_override",
                default=u"Override the default"),
        default=False,
        required=False)

    meta_robots_advanced = schema.List(
        title=_("label_meta_robots_advanced",
                default=u"Meta Robots Advanced Tag"),
        value_type=schema.Choice(
                values=['noodp', 'noydir', 'noarchive', 'nosnippet']
                ),
        required=False)

    meta_robots_advanced_override = schema.Bool(
        title=_("label_title_override",
                default=u"Override the default"),
        default=False,
        required=False)

    canonical = schema.TextLine(
        title=_("label_canonical",
                default=u"Canonical URL"),
        description=_("help_canonical",
                      default=(u"Specify your canonical URL. If your site has "
                          "identical or vastly similar content that's "
                          "accessible through multiple URLs, this format "
                          "provides you with more control over the URL "
                          "returned in search results.")),
        required=False)

    canonical_override = schema.Bool(
        title=_("label_title_override",
                default=u"Override the default"),
        default=False,
        required=False)

    include_in_sitemap = schema.Choice(
        title=_("label_include_in_sitemap",
                default=u"Include in sitemap.xml.gz"),
        values=['yes', 'no'],
        required=False)

    include_in_sitemap_override = schema.Bool(
        title=_("label_title_override",
                default=u"Override the default"),
        default=False,
        required=False)

    sitemap_priority = schema.TextLine(
        title=_("label_sitemap_priority",
                default=u"Sitemap.xml.gz priority"),
        description=_("help_sitemap_priority",
                      default=u"Values from 0.1 to 1.0"),
        required=False)


class ISEOTwitterSettings(Interface):

    twitter_title = schema.TextLine(
        title=_("label_twitter_title",
                default="Twitter title"),
        description=_("help_twitter_title",
                      default=u"i.e. a short title"),
        required=False)

    twitter_description = schema.Text(
        title=_("label_twitter_description",
                default="Twitter description"),
        description=_("help_twitter_description",
                      default=u"i.e. a short site description"),
        required=False)

    twitter_card = schema.Choice(
        title=_("label_twitter_card",
                default="Twitter card"),
        description=_("help_twitter_card",
                      default=u"i.e. summary"),
        values=['summary', 'photo', 'gallery', 'product', 'app', 'player'],
        required=False)

    twitter_site = schema.TextLine(
        title=_("label_twitter_site",
                default="Twitter site"),
        description=_("help_twitter_site",
                      default=u"Site twitter account"),
        required=False)

    twitter_creator = schema.TextLine(
        title=_("label_twitter_creator",
                default="Twitter creator"),
        description=_("help_twitter_creator",
                      default=u"i.e. @redturtle"),
        required=False)

    twitter_image = schema.TextLine(
        title=_("label_twitter_image",
                default="Twitter image"),
        description=_("help_twitter_image",
                      default=u"URL to image preview"),
        required=False)


class ISEOFacebookSettings(Interface):

    facebook_admins = schema.TextLine(
        title=_("label_facebook_admins",
                default="Facebook admins"),
        description=_("help_facebook_admins",
                      default=u"i.e. 1235455444"),
        required=False)

    og_image = schema.TextLine(
        title=_("label_og_image",
                default="Facebook image URL"),
        description=_("help_og_image",
                      default=u"URL to image preview"),
        required=False)

    og_url = schema.TextLine(
        title=_("label_og_url",
                default="Facebook URL"),
        description=_("help_og_url",
                      default=u"URL used by Facebook"),
        required=False)

    og_title = schema.TextLine(
        title=_("label_og_title",
                default="Facebook title"),
        description=_("help_og_title",
                      default=u"Title used by Facebook"),
        required=False)

    og_description = schema.TextLine(
        title=_("label_og_description",
                default="Facebook description"),
        description=_("help_og_description",
                      default=u"Description used by Facebook"),
        required=False)

    og_locale = schema.TextLine(
        title=_("label_og_locale",
                default="Facebook i18n"),
        description=_("help_og_locale",
                      default=u"Locale used by Facebook"),
        required=False)

    og_type = schema.TextLine(
        title=_("label_og_type",
                default="Facebook og:type"),
        description=_("help_og_type",
                      default=u"Type used by Facebook, usually article"),
        required=False)


class ISEOSettings(ISEODefaultSettings, ISEOAdvancedSettings,
        ISEOTwitterSettings, ISEOFacebookSettings):
    """ """
