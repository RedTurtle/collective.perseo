from zope.interface import Interface
from zope import schema
from collective.perseo import perseoMessageFactory as _


class ISEOConfigStructuredDataSchema_homepage(Interface):
    """Schema for Title homepage"""

    homepage_structureddata = schema.Text(
        title=_("label_homepage_structureddata",
                default=u"Home PageStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_searchpage(Interface):
    """Schema for Title searchpage"""

    search_page_structureddata = schema.Text(
        title=_("label_searchpage_structureddata",
                default=u"Search PageStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_notfoundpage(Interface):
    """Schema for Title notfoundpage"""

    notfoundpage_structureddata = schema.Text(
        title=_("label_notfoundpage_structureddata",
                default=u"Not Found PageStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_authorpage(Interface):
    """Schema for Title authorpage"""

    authorpage_structureddata = schema.Text(
        title=_("label_authorpage_structureddata",
                default=u"Author PageStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_sitemappage(Interface):
    """Schema for Title sitemappage"""

    sitemappage_structureddata = schema.Text(
        title=_("label_sitemappage_structureddata",
                default=u"Site mapStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_accessibilitypage(Interface):
    """Schema for Title accessibilitypages"""

    accessibilitypage_structureddata = schema.Text(
        title=_("label_accessibilitypage_structureddata",
                default=u"AccessibilityStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_contactpage(Interface):
    """Schema for Title contactpage"""

    contactpage_structureddata = schema.Text(
        title=_("label_contactpage_structureddata",
                default=u"ContactStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_document(Interface):
    """Schema for Title document"""

    document_structureddata = schema.Text(
        title=_("label_document_structureddata",
                default=u"Single PageStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_event(Interface):
    """Schema for Title event"""

    event_structureddata = schema.Text(
        title=_("label_event_structureddata",
                default=u"EventStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_file(Interface):
    """Schema for Title file"""

    file_structureddata = schema.Text(
        title=_("label_file_structureddata",
                default=u"FileStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_folder(Interface):
    """Schema for Title folder"""

    folder_structureddata = schema.Text(
        title=_("label_folder_structureddata",
                default=u"FolderStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_image(Interface):
    """Schema for Title image"""

    image_structureddata = schema.Text(
        title=_("label_image_structureddata",
                default=u"ImageStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_link(Interface):
    """Schema for Title link"""

    link_structureddata = schema.Text(
        title=_("label_link_structureddata",
                default=u"LinkStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_newsItem(Interface):
    """Schema for Title newsItem"""

    newsitem_structureddata = schema.Text(
        title=_("label_newsItem_structureddata",
                default=u"NewsItemStructured Data"),
        required=False)


class ISEOConfigStructuredDataSchema_topic(Interface):
    """Schema for Title topic"""

    topic_structureddata = schema.Text(
        title=_("label_topic_structureddata",
                default=u"TopicStructured Data"),
        required=False)


class ISeoConfigStructuredDataCheckbox(Interface):
    """ Activate structured data and breadcrumbs"""

    activate_struct_data = schema.Bool(
        title=_("label_activate_structureddata",
                default=u"Activate structured data"),
        description=_("help_activate_structureddata",
                      default=u"Check this checkbox to activate the use of"
                      "structured data"),
        default=False,
        required=False)

    activate_bc_struct_data = schema.Bool(
        title=_("label_activate_breadcrumbs_structureddata",
                default=u"Activate breadcrumb's structured data"),
        description=_("help_activate_breadcrumbs_structureddata",
                      default=u"Check this checkbox to activate the use of"
                      "breadcrumbs related structured data"),
        default=False,
        required=False)


class ISEOConfigStructuredDataSchema(ISeoConfigStructuredDataCheckbox,
                            ISEOConfigStructuredDataSchema_homepage,
                            ISEOConfigStructuredDataSchema_document,
                            ISEOConfigStructuredDataSchema_searchpage,
                            ISEOConfigStructuredDataSchema_notfoundpage,
                            ISEOConfigStructuredDataSchema_authorpage,
                            ISEOConfigStructuredDataSchema_sitemappage,
                            ISEOConfigStructuredDataSchema_accessibilitypage,
                            ISEOConfigStructuredDataSchema_contactpage,
                            ISEOConfigStructuredDataSchema_event,
                            ISEOConfigStructuredDataSchema_file,
                            ISEOConfigStructuredDataSchema_folder,
                            ISEOConfigStructuredDataSchema_image,
                            ISEOConfigStructuredDataSchema_link,
                            ISEOConfigStructuredDataSchema_newsItem,
                            ISEOConfigStructuredDataSchema_topic):
    """Schema for Title"""


#def add_fields_to_ISEOConfigStructuredDataSchema(fields):
#    for field in fields:
#        title = field.capitalize()
#        structureddata = schema.Text(
#            title=_("label_%s_structureddata" % field,
#                    default=u"%s structured data" % title),
#            required=False)
#
#        structureddata.__name__ = '%s_structured_data' % title
#        structureddata.interface = ISEOConfigStructuredDataSchema
#        ISEOConfigStructuredDataSchema._InterfaceClass__attrs[structureddata.__name__] = structureddata
