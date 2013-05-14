from Acquisition import aq_inner
from zope.annotation.interfaces import IAnnotations, IAnnotatable
from zope.component import getUtility
from zope.component import queryMultiAdapter
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

try:
    from Products.LinguaPlone.interfaces import ITranslatable
    LINGUA_PLONE = True
except ImportError:
    LINGUA_PLONE = False

from collective.perseo.interfaces import ISEOControlpanel
from collective.perseo import PERSEO


class PloneSiteSeoContextAdapter(object):

    def __init__(self, context):
        registry = getUtility(IRegistry)
        self.context = context
        self.settings = registry.forInterface(ISEOControlpanel)
        self.pm = getToolByName(self.context, 'portal_membership')
        self.pcs = queryMultiAdapter((self.context, context.REQUEST), name="plone_context_state")
        self.pps = queryMultiAdapter((self.context, context.REQUEST), name="plone_portal_state")

    def get(self, name):
        context = aq_inner(self.context)
        if not IAnnotatable.providedBy(self.context):
            return None
        annotations = IAnnotations(context)
        if annotations.has_key(PERSEO):
            return annotations[PERSEO].get(name, None)
        return None

    def find_robots_context(self):
        template_id = None
        if 'PUBLISHED' in self.context.REQUEST:
            if getattr(self.context.REQUEST['PUBLISHED'], 'getId', None):
                # template inside skins
                template_id = self.context.REQUEST['PUBLISHED'].getId()
            if getattr(self.context.REQUEST['PUBLISHED'], __name__, None):
                # template inside browser view
                template_id = self.context.REQUEST['PUBLISHED'].__name__

        if template_id:
            if template_id == 'search' or template_id == 'search_form':
                return 'searchpage'
            elif 'login' in template_id \
                or 'logout' in template_id \
                or 'logged' in template_id \
                or 'registered' in template_id:
                return 'loginregistrationpage'
            elif template_id == 'plone_control_panel':
                return 'administrationpage'
            else:
                return None
        else:
            return None

    def find_context(self):
        # I take template_id as is done in ploneview
        # if all goes well for ploneview is fine in my general view
        template_id = None
        if 'PUBLISHED' in self.context.REQUEST:
            if getattr(self.context.REQUEST['PUBLISHED'], 'getId', None):
                # template inside skins
                template_id = self.context.REQUEST['PUBLISHED'].getId()
            if getattr(self.context.REQUEST['PUBLISHED'], __name__, None):
                # template inside browser view
                template_id = self.context.REQUEST['PUBLISHED'].__name__

        if template_id:
            if template_id == 'search' or template_id == 'search_form':
                return 'searchpage'
            elif template_id == 'author':
                return 'authorpage'
            elif template_id == 'sitemap':
                return 'sitemappage'
            elif template_id == 'accessibility-info':
                return 'accessibilitypage'
            elif template_id == 'contact-info':
                return 'contactpage'
            else:
                return 'homepage'
        else:
            try:
                self.context.restrictedTraverse(self.context.REQUEST.PATH_INFO)
            except:
                return 'notfoundpage'
            return 'homepage'

    @property
    def title(self):
        if not self.title_override:
            return self.pcs.object_title()
        page = self.find_context()
        return self.get('title') or \
               getattr(self.settings, '%s_title' % page) or \
               self.pcs.object_title()

    @property
    def title_override(self):
        return False

    @property
    def description(self):
        context = aq_inner(self.context)
        if not self.description_override:
            return context.Description() or ''
        page = self.find_context()
        return self.get('description') or \
               getattr(self.settings, '%s_description' % page) or \
               context.Description()

    @property
    def description_override(self):
        return False

    @property
    def keywords(self):
        context = aq_inner(self.context)
        if not self.keywords_override:
            return context.Subject() or ''
        page = self.find_context()
        return self.get('keywords') or \
               getattr(self.settings, '%s_keywords' % page) or \
               context.Subject()

    @property
    def keywords_override(self):
        return False

    @property
    def meta_robots_follow(self):
        page = self.find_robots_context()
        return getattr(self.settings, 'indexing_%s' % page) \
                                                    and 'nofollow' or 'follow'

    @property
    def meta_robots_index(self):
        page = self.find_robots_context()
        return getattr(self.settings, 'indexing_%s' % page) \
                                                    and 'noindex' or 'index'

    @property
    def canonical_override(self):
        return False

    @property
    def include_in_sitemap(self):
        if not self.include_in_sitemap_override:
            return False
        return self.get('include_in_sitemap')

    @property
    def include_in_sitemap_override(self):
        return False

    @property
    def alternate_i18n(self):
        """ Return available translations if LinguaPlone is available """
        if LINGUA_PLONE and ITranslatable.providedBy(self.context):
            translations = self.context.getTranslations(review_state=False)
            if self.context.Language() in translations:
                del translations[self.context.Language()]
            return translations
        else:
            return []

    @property
    def bingWebmasterTools(self):
        return self.settings.bingWebmasterTools

    @property
    def googleWebmasterTools(self):
        return self.settings.googleWebmasterTools

    # Twitter stuff
    @property
    def twitter_card(self):
        return self.get('twitter_card') or 'summary'

    @property
    def twitter_site(self):
        return self.settings.twitter_site

    @property
    def twitter_creator(self):
        author = self.pm.getMemberById(self.context.Creator())
        return self.get('twitter_creator') or \
            author and author.getProperty('twitter_author') or ''

    @property
    def twitter_description(self):
        return self.get('twitter_description') or self.description

    @property
    def twitter_title(self):
        return self.get('twitter_title') or self.title

    @property
    def twitter_image(self):
        return self.get('twitter_image') or self.og_image

    # Facebook stuff
    @property
    def facebook_admins(self):
        return self.settings.facebook_admins

    @property
    def og_site_name(self):
        return self.settings.og_site_name

    @property
    def og_locale(self):
        return self.get('og_locale') or self.context.Language()

    @property
    def og_type(self):
        return self.get('og_type') or 'article'

    @property
    def og_title(self):
        return self.get('og_title') or self.title

    @property
    def og_description(self):
        return self.get('og_description') or self.description

    @property
    def og_url(self):
        return self.get('og_url') or self.canonical

    @property
    def og_image(self):
        return self.get('og_image') or '%s/logo.png' % self.context.absolute_url()
