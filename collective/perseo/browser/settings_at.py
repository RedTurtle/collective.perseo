from Acquisition import aq_inner
from zope.interface import implements
from zope.component import getUtility
from zope.component import queryMultiAdapter
from zope.annotation.interfaces import IAnnotations
from plone.registry.interfaces import IRegistry
try:
    from Products.LinguaPlone.interfaces import ITranslatable
    LINGUA_PLONE = True
except ImportError:
    LINGUA_PLONE = False

from collective.perseo.interfaces import ISEOConfigSchema
from collective.perseo.interfaces.settings import ISEOContextAdvancedSchema,\
        ISEOContextMetaSchema

PERSEO = 'collective.perseo'


class ATSeoContextAdapter(object):

    def __init__(self, context):
        self.context = context
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ISEOConfigSchema)
        self.pcs = queryMultiAdapter((self.context, context.REQUEST), name="plone_context_state")
        self.pps = queryMultiAdapter((self.context, context.REQUEST), name="plone_portal_state")

    def get(self, name):
        context = aq_inner(self.context)
        annotations = IAnnotations(context)
        if annotations.has_key(PERSEO):
            return annotations[PERSEO].get(name, None)
        return None

    def find_context(self):
        try:
            self.context.restrictedTraverse(self.context.REQUEST.PATH_INFO)
        except:
            return 'notfoundpage'

        context = self.pcs.context
        parent = self.pcs.parent()

        if parent == self.pps.portal() and parent.getDefaultPage() == context.id:
            return 'homepage'
        else:
            return self.portal_type


class ATSeoContextMetaAdapter(ATSeoContextAdapter):

    implements(ISEOContextMetaSchema)

    @property
    def portal_type(self):
        return self.pcs.context.portal_type.lower()

    @property
    def title(self):
        page = self.find_context()
        return self.get('title') or \
               getattr(self.settings, '%s_title' % page) or \
               self.pcs.object_title()

    @property
    def title_override(self):
        return self.get('title_override')

    @property
    def description(self):
        page = self.find_context()
        context = aq_inner(self.context)
        return self.get('description') or \
               getattr(self.settings, '%s_description' % page) or \
               context.Description()

    @property
    def description_override(self):
        return self.get('description_override')

    @property
    def keywords(self):
        page = self.find_context()
        context = aq_inner(self.context)
        return self.get('keywords') or \
               getattr(self.settings, '%s_keywords' % page) or \
               context.Subject()

    @property
    def keywords_override(self):
        return self.get('keywords_override')


class ATSeoContextAdvancedAdapter(ATSeoContextAdapter):

    implements(ISEOContextAdvancedSchema)

    @property
    def meta_robots_follow(self):
        perseo_property = self.get('meta_robots_follow')
        if perseo_property:
            return perseo_property
        return getattr(self.settings, 'indexing_%s' % self.portal_type) \
                                                    and 'nofollow' or 'follow'

    @property
    def meta_robots_follow_override(self):
        return self.get('meta_robots_follow_override')

    @property
    def meta_robots_index(self):
        perseo_property = self.get('meta_robots_index')
        if perseo_property:
            return perseo_property
        return getattr(self.settings, 'indexing_%s' % self.portal_type) \
                                                    and 'noindex' or 'index'

    @property
    def meta_robots_index_override(self):
        return self.get('meta_robots_index_override')

    @property
    def meta_robots_advanced(self):
        return self.get('meta_robots_advanced')

    @property
    def meta_robots_advanced_override(self):
        return self.get('meta_robots_advanced_override')

    @property
    def canonical(self):
        return self.get('canonical')

    @property
    def canonical_override(self):
        return self.get('canonical_override')

    @property
    def include_in_sitemap(self):
        return self.get('include_in_sitemap')

    @property
    def include_in_sitemap_override(self):
        return self.get('include_in_sitemap_override')

    @property
    def sitemap_priority(self):
        return self.get('sitemap_priority')

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
