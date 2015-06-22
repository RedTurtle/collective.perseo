from Products.CMFPlone.utils import safe_unicode
from collective.perseo.browser.settings_plone import PloneSiteSeoContextAdapter
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

BASE_TYPE = map(str.lower, ['Document', 'Event', 'File', 'Image', 'Link', 'News Item', 'Topic', 'Collection'])


class ATSeoContextAdapter(PloneSiteSeoContextAdapter):

    def find_context(self):
        #FIX: it's really ugly.
        # 'maybe' we have a published site so it's better to use VIRTUAL_URL_PARTS
        # on local it's ok PATH_INF
        path = None
        if 'VIRTUAL_URL_PARTS' in self.context.REQUEST:
            path = self.context.REQUEST.VIRTUAL_URL_PARTS[-1]
        else:
            path = self.context.REQUEST.PATH_INFO

        try:
            self.context.restrictedTraverse(path)
        except:
            try:
                #maybe we are searching for author page
                path = '/'.join(path.split('/')[:-1])
                self.context.restrictedTraverse(path)
                if not path.endswith('/author'):
                    return 'notfoundpage'

            except:
                return 'notfoundpage'

        context = self.pcs.context
        parent = self.pcs.parent()

        # Be careful: if we have LinguaPlone, all the view are not on the root
        # But they are on a context. So if we have one of those template id,
        # return it
        template_id = None
        if 'PUBLISHED' in self.context.REQUEST:
            if getattr(self.context.REQUEST['PUBLISHED'], 'getId', None):
                # template inside skins
                template_id = self.context.REQUEST['PUBLISHED'].getId()
            if getattr(self.context.REQUEST['PUBLISHED'], '__name__', None):
                # template inside browser view
                template_id = self.context.REQUEST['PUBLISHED'].__name__

        if template_id in ('search', 'search_form', ):
            return 'search_page'
        elif template_id in ('author', ):
            return 'authorpage'
        elif template_id in ('sitemap', ):
            return 'sitemap'
        elif template_id in ('accessibility-info'):
            return 'accessibilitypage'
        elif template_id in ('contact-info'):
            return 'contactpage'
        elif template_id in ('plone_control_panel', 'overview-controlpanel'):
                return 'administration_page'
        elif 'login' in template_id \
                or 'logout' in template_id \
                or 'logged' in template_id \
                or 'registered' in template_id \
                or 'register' in template_id:
            return 'login_registration_page'

        # we could have also LinguaPlone and different level of navigation root: site root
        # and language root
        if (parent == self.pps.portal() and parent.getDefaultPage() == context.id) or \
           (self.pps.navigation_root() == context) or \
           (parent == self.pps.navigation_root() and parent.getDefaultPage() == context.id):
            return 'homepage'
        else:
            # BBB To fix in a better way. We should have something like a mapper to map custom type
            # over standard type
            type_mapper = self.get_type_mapper()
            # import pdb; pdb.set_trace()
            if not self.portal_type in BASE_TYPE and ('default' in type_mapper or self.portal_type in type_mapper):
                result = self.portal_type in type_mapper and type_mapper[self.portal_type] or type_mapper['default']
                return result.replace(' ', '')

            if ' ' in self.portal_type:
                return self.portal_type.replace(' ', '')
            return self.portal_type

    def get_type_mapper(self):
        registry = queryUtility(IRegistry)
        settings = registry.records['perseo_type_mapper']
        types = settings.value.strip().split('\r\n')
        if not types:
            return ""
        res = {}
        for ty in types:
            k, v = ty.split('#')
            res[k.lower()] = v.lower()
        return res

    @property
    def portal_type(self):
        return self.pcs.context.portal_type.lower()

    @property
    def robots(self):
        self.robot_context = self.find_context()
        override = getattr(self.settings, 'meta_robots_index_override_%s' % self.robot_context, False)
        if not override:
            return u''
        result = (self.meta_robots_follow, self.meta_robots_index,
                  ', '.join(self.meta_robots_advanced))
        self.robot_context = None
        return safe_unicode(result)

    @property
    def meta_robots_follow(self):
        if self.meta_robots_follow_override:
            perseo_property = self.get('meta_robots_follow')
            if perseo_property:
                return perseo_property
        override = getattr(self.settings, 'meta_robots_index_override_%s' % self.robot_context, False)  # override?
        if override:
            result = getattr(self.settings, 'meta_robots_follow_%s' % self.robot_context, None) \
                 or 'follow'
            return safe_unicode(result)
        return 'follow'

    @property
    def meta_robots_index(self):
        if self.meta_robots_index_override:
            perseo_property = self.get('meta_robots_index')
            if perseo_property:
                return perseo_property
        override = getattr(self.settings, 'meta_robots_index_override_%s' % self.robot_context, False)  # override?
        if override:
            result = getattr(self.settings, 'meta_robots_index_%s' % self.robot_context, None) \
                 or 'index'
            return safe_unicode(result)
        return 'index'

    @property
    def meta_robots_advanced(self):
        if self.meta_robots_index_override:
            perseo_property = self.get('meta_robots_advanced')
            if perseo_property:
                return perseo_property
        override = getattr(self.settings, 'meta_robots_index_override_%s' % self.robot_context, False)  # override?
        if override:
            site_globals = getattr(self.settings, "meta_robots_advanced_%s" % self.robot_context)
            result = self.get('meta_robots_advanced') or site_globals or ()
            return result
        return ()
