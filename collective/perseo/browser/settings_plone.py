from Acquisition import aq_inner
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from zope.component import queryMultiAdapter
from collective.perseo.interfaces import ISEOConfigSchema


class PloneSiteSeoContextAdapter(object):

    def __init__(self, context):
        registry = getUtility(IRegistry)
        self.context = context
        self.settings = registry.forInterface(ISEOConfigSchema)
        self.pcs = queryMultiAdapter((self.context, context.REQUEST), name="plone_context_state")

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
        return getattr(self.settings, '%s_title' % page) or \
               self.pcs.object_title()

    @property
    def title_override(self):
        return True

    @property
    def description(self):
        page = self.find_context()
        context = aq_inner(self.context)
        return getattr(self.settings, '%s_description' % page) or \
               context.Description()

    @property
    def keywords(self):
        page = self.find_context()
        context = aq_inner(self.context)
        return getattr(self.settings, '%s_keywords' % page) or \
               context.Subject()

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
    def alternate_i18n(self):
        return []
