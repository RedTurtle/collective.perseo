from z3c.form import field
from plone.app.registry.browser import controlpanel
from plone.z3cform.fieldsets import group
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName

from collective.perseo import perseoMessageFactory as _
from collective.perseo.interfaces import ISEOControlpanel
from collective.perseo.interfaces.metaconfig import ISEOConfigTitleSchema
from collective.perseo.interfaces.structureddata import ISEOConfigStructuredDataSchema
from collective.perseo.interfaces.controlpanel import (ISEOConfigSiteMapXMLSchema,
                                                       ISEOConfigIndexingSchema,
                                                       IHrefLangSchema,
                                                       ISEOConfigSocialSchema)


class HrefLangForm(group.Group):
    label = _(u"Hreflang settings")
    description = _(u"If LinguaPlone is installed below you can activate options for hreflang link tag in header")
    fields = field.Fields(IHrefLangSchema)


class TitleForm(group.Group):
    label = _(u"Type headers")
    description = _(u"Here you can override at global level value for title, description and keywords for different types and templates."
                    " In these box you can use variables like: %%title%%', '%%tag%%', '%%description%%', '%%startdate%%', '%%enddate%%',"
                    " '%%sitename%%', '%%fullname%%', '%%searchedtext%%. 'title', 'tag' and 'description' are taken from the context you"
                    " are looking. If your context it's an event, you can use 'startdata' and 'enddate'. If you are in the author page,"
                    " you can use 'fullname' to use the author fullname or, if you are on a content, you can get the authors list. If"
                    " you are customizing search page, you can use 'searchedtext' to take the search query string")
    fields = field.Fields(ISEOConfigTitleSchema)


class StructuredDataForm(group.Group):
    label = _(u"Structured Data")
    description = _(u"")
    fields = field.Fields(ISEOConfigStructuredDataSchema)


class SitemapForm(group.Group):
    label = _(u"Sitemap")
    description = _(u"Handle how sitemap will be generated; remember to flag enable_sitemap in site_properties")
    fields = field.Fields(ISEOConfigSiteMapXMLSchema)


class IndexingForm(group.Group):
    label = _(u"Indexing")
    description = _(u"Handle how different types with be index by robots")
    fields = field.Fields(ISEOConfigIndexingSchema)


class SocialForm(group.Group):
    label = _(u"Social networks")
    description = _(u"Handle how your site will be indexed by social networks")
    fields = field.Fields(ISEOConfigSocialSchema)


class PerSEOSettingsEditForm(controlpanel.RegistryEditForm):

    label = _(u"PerSEO settings")
    description = _(u"")
    schema = ISEOControlpanel
    groups = (SitemapForm, IndexingForm, SocialForm, TitleForm, HrefLangForm, StructuredDataForm)

    def updateFields(self):
        super(PerSEOSettingsEditForm, self).updateFields()
        have_lp = self.check_product('LinguaPlone')
        if not have_lp:
            for group in self.groups:
                if group.__name__ == 'HrefLangForm':
                    group.fields._data_values = []
        #To fix: still have problems with this saving the form
        #have_ps = self.check_product('collective.perseoschema')
        #if not have_ps:
        #    fields = []
        #    for field in self.fields._data_values:
        #        if field.__name__ == 'itemscope_itemtype_attrs_enable':
        #            continue
        #        else:
        #            fields.append(field)
        #    self.fields._data_values = fields
        #    del self.fields._data['itemscope_itemtype_attrs_enable']

    def check_product(self, product):
        qi = getToolByName(self.context, 'portal_quickinstaller')
        prods = qi.listInstallableProducts(skipInstalled=False)
        for prod in prods:
            if (prod['id'] == product) and (prod['status'] == 'installed'):
                return True


class PerSEOControlPanel(controlpanel.ControlPanelFormWrapper):
    form = PerSEOSettingsEditForm


class PerSEORSS(BrowserView):

    def __call__(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISEOControlpanel)
        return {'indexing_feed_rss': settings.indexing_feed_rss}
