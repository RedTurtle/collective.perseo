from zope.interface import Interface
from zope import schema
from collective.perseo import perseoMessageFactory as _


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

    search_page_title = schema.TextLine(
        title=_("label_searchpage_title",
                default=u"Search Page Title"),
        required=False)

    search_page_description = schema.Text(
        title=_("label_searchpage_description",
                default=u"Search Page Description"),
        required=False)

    search_page_keywords = schema.List(
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

    newsitem_title = schema.TextLine(
        title=_("label_newsItem_title",
                default=u"NewsItem Title"),
        required=False)

    newsitem_description = schema.Text(
        title=_("label_newsItem_description",
                default=u"NewsItem Description"),
        required=False)

    newsitem_keywords = schema.List(
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
