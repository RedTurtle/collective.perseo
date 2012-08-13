import re
import zope.event

from zope.schema.interfaces import InvalidValue
from zope.component import queryAdapter
from zope.component import queryMultiAdapter
from zope.annotation.interfaces import IAnnotations

from Acquisition import aq_inner
from DateTime import DateTime
from Products.Five.browser import BrowserView
from Products.Archetypes.event import ObjectEditedEvent
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.perseo import perseoMessageFactory as _
from collective.perseo.browser.seo_config import ISEOConfigSchema

PERSEO_PREFIX = 'perseo_'
SUFFIX = '_override'
PROP_PREFIX = 'pSEO_'


class PerSEOTabContext( BrowserView ):
    "This class contains methods that allows to manage SEO tab."

    template = ViewPageTemplateFile('templates/perseo_tab_context.pt')

    def __init__(self, *args, **kwargs):
        super(PerSEOTabContext, self).__init__(*args, **kwargs)
        self.pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        self.gseo = queryAdapter(self.pps.portal(), ISEOConfigSchema)

    def setProperty(self, property, value):
        """Add a new item to annotation.
           Sets a new item with the given key, value or changes it."""

        state = False
        context = aq_inner(self.context)
        annotations = IAnnotations(context)
        if property in annotations:
            current_value = annotations.get(property, None)
            if value != current_value:
                state = True
            annotations[property] = value
            if (property == 'pSEO_included_in_sitemapxml' or property == 'pSEO_priority_sitemapxml')\
                and state:
                context.reindexObject(idxs=[])
        else:
            state = True
            annotations[property] = value

        return state

    def delProperties(self, delete_list):
        """ Delete some items to annotation.
        """
        context = aq_inner(self.context)
        annotations = IAnnotations(context)
        for property in delete_list:
            annotations.pop(property)

    def manageSEOProps(self, **kw):
        """ Manage seo properties.
        """
        description = {}
        state = False
        context = aq_inner(self.context)
        annotations = IAnnotations(context)

        delete_list, perseo_overrides_keys, perseo_keys = [], [], []
        seo_items = dict([(k[len(PERSEO_PREFIX):],v) for k,v in kw.items() if k.startswith(PERSEO_PREFIX)])
        for key in seo_items.keys():
            if key.endswith(SUFFIX):
                perseo_overrides_keys.append(key[:-len(SUFFIX)])
            else:
                perseo_keys.append(key)

        for perseo_key in perseo_keys:
            if perseo_key in perseo_overrides_keys and seo_items.get(perseo_key+SUFFIX):
                perseo_value = seo_items[perseo_key]
                if perseo_value:
                    if perseo_key == "robots_advanced" and '' in perseo_value:
                        perseo_value.remove('')
                    if perseo_key=="included_in_sitemapxml":
                        if perseo_value == 'no':
                            perseo_value = False
                        else:
                            perseo_value = True
                if perseo_key=="priority_sitemapxml":
                    if perseo_value == '' and not PROP_PREFIX+perseo_key in annotations:
                        continue
                    perseo_value = perseo_value and float(perseo_value) or perseo_value
                if self.setProperty(PROP_PREFIX+perseo_key, perseo_value):
                    state = True
                    if perseo_key == 'included_in_sitemapxml' or perseo_key == 'priority_sitemapxml':
                        description[perseo_key] = perseo_value
            elif PROP_PREFIX+perseo_key in annotations:
                delete_list.append(PROP_PREFIX+perseo_key)
        if delete_list:
            state = True
            self.delProperties(delete_list)

        if description:
            # Cases in which the sitemap.xml is modified:
            # pSEO_included_in_sitemapxml property is updated --> A new entry is inserted/removed in the sitemap.xml
            # pSEO_priority_sitemapxml property is updated --> The priority property of sitemap.xml is changed
            event = ObjectEditedEvent(context, description)
            zope.event.notify(event)

        return state

    def canonical_validate(self, value):
        # non space and no new line(should be pickier)
        _is_canonical = re.compile(r"\S*$").match

        if not _is_canonical(value):
            raise InvalidValue(value)

    def validate(self,form):
        msg = []
        if form.has_key(PERSEO_PREFIX+'canonical') \
            and form.has_key(PERSEO_PREFIX+'canonical'+SUFFIX)\
            and form.get(PERSEO_PREFIX+'canonical'+SUFFIX):
            canonical_url = form.get(PERSEO_PREFIX+'canonical')
            try:
                self.canonical_validate(canonical_url)
            except InvalidValue, e:
                msg.append(_(u"wrong_canonical_url", 
                             default=u'The Canonical URL "${url}" is incorrect',
                             mapping={'url':str(e)}))
        if form.has_key(PERSEO_PREFIX+'priority_sitemapxml')\
            and form.get(PERSEO_PREFIX+'priority_sitemapxml'):
            priority_sitemapxml = form.get(PERSEO_PREFIX+'priority_sitemapxml')
            try:
                priority_sitemapxml = float(priority_sitemapxml)
                if priority_sitemapxml < 0.1:
                    msg.append(_(u"wrong_priority_sitemapxml_greater", 
                                 default=u"The Priority sitemap.xml.gz need to be greater than 0.0"))
                if priority_sitemapxml > 1.0:
                    msg.append(_(u"wrong_priority_sitemapxml_less", 
                                 default=u"The Priority sitemap.xml.gz need to be less than or equal to 1.0"))
            except ValueError, e:
                msg.append(_(u"wrong_priority_sitemapxml", 
                             default=u"The Priority sitemap.xml.gz must be a number"))
        return msg

    def __call__( self ):
        """ Perform the update SEO properties and redirect if necessary,
            or render the template.
        """
        request = self.request
        form = request.form

        portal_properties = getToolByName(self.context, 'portal_properties')
        use_view_action = portal_properties.site_properties.typesUseViewActionInListings
        item_type = self.context.portal_type
        item_url = self.context.absolute_url()
        redirect_url = item_type in use_view_action and item_url+'/view' or item_url

        if form.get('form.button.Cancel', False):
            return request.response.redirect(redirect_url)

        if form.get('form.button.Save', False):
            context = aq_inner(self.context)
            msgs = self.validate(form)
            if msgs:
                for msg in msgs:
                    context.plone_utils.addPortalMessage(msg, 'error')
                return self.template()
            state = self.manageSEOProps(**form)
            if state:
                state = _('perseo_settings_saved', default=u'The SEO settings have been saved.')
                context.plone_utils.addPortalMessage(state)
                kwargs = {'modification_date' : DateTime()}
                context.plone_utils.contentEdit(context, **kwargs)
            return request.response.redirect(redirect_url)

        return self.template()
