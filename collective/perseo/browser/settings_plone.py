from Acquisition import aq_inner
from zope.annotation.interfaces import IAnnotations, IAnnotatable
from zope.component import getUtility
from zope.component import queryMultiAdapter
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

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
        # first check overrides if exists and is True
        overrides = getattr(self, '%s_override' % name, True)
        if not overrides:
            return None

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
        page = self.find_context()
        result = self.get('title') or \
                 getattr(self.settings, '%s_title' % page, None) or \
                 self.pcs.object_title()
        return safe_unicode(result)

    @property
    def description(self):
        context = aq_inner(self.context)
        page = self.find_context()
        result = self.get('description') or \
                 getattr(self.settings, '%s_description' % page, None) or \
                 context.Description()
        return safe_unicode(result)

    @property
    def keywords(self):
        context = aq_inner(self.context)
        page = self.find_context()
        result = self.get('keywords') or \
               getattr(self.settings, '%s_keywords' % page, None) or \
               context.Subject()
        return safe_unicode(result)

    @property
    def meta_robots_follow(self):
        page = self.find_robots_context()
        result = getattr(self.settings, 'indexing_%s' % page, None) \
                                                    and 'nofollow' or 'follow'
        return safe_unicode(result)

    @property
    def meta_robots_index(self):
        page = self.find_robots_context()
        result = getattr(self.settings, 'indexing_%s' % page, None) \
                                                    and 'noindex' or 'index'
        return safe_unicode(result)
    @property
    def meta_robots_advanced(self):
        site_globals = self.settings.meta_robots_advanced
        result = self.get('meta_robots_advanced') or site_globals or ()
        return result

    @property
    def robots(self):
        result = (self.meta_robots_follow, self.meta_robots_index,
                ', '.join(self.meta_robots_advanced))
        return safe_unicode(result)

    @property
    def canonical(self):
        result = self.get('canonical') or ''
        return safe_unicode(result)

    @property
    def sitemap_priority(self):
        result = self.get('sitemap_priority')
        return safe_unicode(result)

    @property
    def include_in_sitemap(self):
        return self.get('include_in_sitemap') or False

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
        result = self.settings.bingWebmasterTools
        return safe_unicode(result)

    @property
    def googleWebmasterTools(self):
        result = self.settings.googleWebmasterTools
        return safe_unicode(result)

    @property
    def meta_robots_index_override(self):
        return self.get('meta_robots_index_override') or False

    @property
    def meta_robots_follow_override(self):
        return self.get('meta_robots_follow_override') or False

    @property
    def title_override(self):
        return self.get('title_override') or False

    @property
    def description_override(self):
        return self.get('description_override') or False

    @property
    def keywords_override(self):
        return self.get('keywords_override') or False

    @property
    def meta_robots_advanced_override(self):
        return self.get('meta_robots_advanced_override') or False

    @property
    def canonical_override(self):
        return self.get('canonical_override') or False

    @property
    def include_in_sitemap_override(self):
        return self.get('include_in_sitemap_override') or False

    # Twitter stuff
    @property
    def twitter_card(self):
        result = self.get('twitter_card') or 'summary'
        return safe_unicode(result)

    @property
    def twitter_card_override(self):
        return self.get('twitter_card_override') or False

    @property
    def twitter_site(self):
        result = self.settings.twitter_site
        return safe_unicode(result)

    @property
    def twitter_creator(self):
        author = self.pm.getMemberById(self.context.Creator())
        result = self.get('twitter_creator') or \
            author and author.getProperty('twitter_author') or ''
        return safe_unicode(result)

    @property
    def twitter_creator_override(self):
        return self.get('twitter_creator_override') or False

    @property
    def twitter_description(self):
        result = self.get('twitter_description') or self.description
        return safe_unicode(result)

    @property
    def twitter_description_override(self):
        return self.get('twitter_description_override') or False

    @property
    def twitter_title(self):
        result = self.get('twitter_title') or self.title
        return safe_unicode(result)

    @property
    def twitter_title_override(self):
        return self.get('twitter_title_override') or False

    @property
    def twitter_image(self):
        return self.get('twitter_image') or self.og_image

    @property
    def twitter_image_override(self):
        return self.get('twitter_image_override') or False

    # Facebook stuff
    @property
    def facebook_admins(self):
        result = self.settings.facebook_admins
        return safe_unicode(result)

    @property
    def og_site_name(self):
        result = self.settings.og_site_name
        return safe_unicode(result)

    @property
    def og_locale(self):
        result = self.get('og_locale') or self.context.Language()
        return safe_unicode(result)

    @property
    def og_locale_override(self):
        return self.get('og_locale_override') or False

    @property
    def og_type(self):
        result = self.get('og_type') or 'article'
        return safe_unicode(result)

    @property
    def og_type_override(self):
        return self.get('og_type_override') or False

    @property
    def og_title(self):
        result = self.get('og_title') or self.title
        return safe_unicode(result)

    @property
    def og_title_override(self):
        return self.get('og_title_override') or False

    @property
    def og_description(self):
        result = self.get('og_description') or self.description
        return safe_unicode(result)

    @property
    def og_description_override(self):
        return self.get('og_description_override') or False

    @property
    def og_url(self):
        result = self.get('og_url') or self.canonical
        return safe_unicode(result)

    @property
    def og_url_override(self):
        return self.get('og_url_override') or False

    @property
    def og_image(self):
        result = self.get('og_image') or '%s/logo.png' % self.context.absolute_url()
        return safe_unicode(result)

    @property
    def og_image_override(self):
        return self.get('og_image_override') or False
