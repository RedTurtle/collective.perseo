from ZODB.PersistentMapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations, IAnnotatable
from zope.interface import implements
from z3c.form import form, field, button
from z3c.form.browser.radio import RadioFieldWidget
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot
from plone.z3cform.layout import wrap_form
from plone.z3cform.fieldsets import extensible
from plone.z3cform.fieldsets import group

from collective.perseo.interfaces.settings import ISEOSettings, \
        ISEOAdvancedSettings, ISEOTwitterSettings, ISEOFacebookSettings
from collective.perseo import perseoMessageFactory as _

PERSEO = 'collective.perseo'


class SEOContextAdvancedForm(group.Group):
    fields = field.Fields(ISEOAdvancedSettings)
    label = _(u"Advanced settings")
    fields['include_in_sitemap'].widgetFactory = RadioFieldWidget
    fields['meta_robots_follow'].widgetFactory = RadioFieldWidget
    fields['meta_robots_index'].widgetFactory = RadioFieldWidget


class SEOContextTwitterForm(group.Group):
    fields = field.Fields(ISEOTwitterSettings).select('twitter_card',
            'twitter_card_override', 'twitter_creator',
            'twitter_creator_override', 'twitter_title',
            'twitter_title_override', 'twitter_description', 
            'twitter_description_override',
            'twitter_image', 'twitter_image_override')
    label = _(u"Twitter settings")

    def updateWidgets(self):
        super(SEOContextTwitterForm, self).updateWidgets()
        self.widgets['twitter_description'].cols = 40
        self.widgets['twitter_description'].rows = 5


class SEOContextFacebookForm(group.Group):
    fields = field.Fields(ISEOFacebookSettings).select('og_title', 
            'og_title_override', 'og_description', 'og_description_override',
            'og_url', 'og_url_override', 'og_locale', 
            'og_locale_override', 'og_image', 'og_image_override', 'og_type',
            'og_type_override')
    label = _(u"Facebook settings")

    def updateWidgets(self):
        super(SEOContextFacebookForm, self).updateWidgets()
        self.widgets['og_description'].cols = 40
        self.widgets['og_description'].rows = 5


class SEOContextForm(extensible.ExtensibleForm, form.Form):
    implements(ISEOSettings)

    form_name = "perseo_context_settings"
    id = 'perseo-context-settings-form'
    description = _(u"Manage SEO settings for this content")
    groups = (SEOContextTwitterForm, SEOContextFacebookForm, SEOContextAdvancedForm,)
    ignoreContext = False
    message_ok = _(u'Changes saved.')
    message_cancel = _(u'No changes made.')
    fields = field.Fields(ISEOSettings).select('title', 'title_override', 
       'description', 'description_override', 'keywords', 'keywords_override')

    @property
    def next_url(self):
        return self.context.absolute_url()

    def redirectAction(self):
        self.request.response.redirect(self.next_url)

    def setStatusMessage(self, message, level='info'):
        ptool = getToolByName(self.context, 'plone_utils')
        ptool.addPortalMessage(message, level)

    def updateWidgets(self):
        super(SEOContextForm, self).updateWidgets()
        self.widgets['keywords'].cols = 15
        self.widgets['keywords'].rows = 11
        self.widgets['description'].cols = 40
        self.widgets['description'].rows = 5

    @button.buttonAndHandler(_(u'Save'))
    def handleApply(self, action):  # pylint: disable=W0613
        data, errors = self.extractData()
        if (errors):
            return

        annotations = IAnnotations(self.context)
        annotations[PERSEO] = PersistentMapping()
        for k,v in data.items():
            if v:
                annotations[PERSEO][k] = v

        self.setStatusMessage(self.message_ok)
        self.redirectAction()

    @button.buttonAndHandler(_(u'Cancel'))
    def handleCancel(self, action):  # pylint: disable=W0613
        self.setStatusMessage(self.message_cancel)
        self.redirectAction()


manageSEOContext = wrap_form(
        SEOContextForm,
        label=_(u'PerSEO settings'),
        description=_(u'Manage PerSEO settings for this content.')
        )


class PerseoTabAvailable(BrowserView):

    def checkPerseoTabAvailable(self):
        """ Checks visibility of SEO tab for context
        """
        return not IPloneSiteRoot.providedBy(self.context) and \
                IAnnotatable.providedBy(self.context)
