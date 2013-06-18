from Products.CMFPlone.utils import safe_unicode
from collective.perseo.browser.settings_plone import PloneSiteSeoContextAdapter


class ATSeoContextAdapter(PloneSiteSeoContextAdapter):

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

    @property
    def portal_type(self):
        return self.pcs.context.portal_type.lower()

    @property
    def meta_robots_follow(self):
        if self.meta_robots_follow_override:
            perseo_property = self.get('meta_robots_follow')
            if perseo_property:
                return perseo_property
        override = getattr(self.settings, 'meta_robots_index_override_%s' % self.portal_type, False)  # override?
        if override:
            result = getattr(self.settings, 'meta_robots_follow_%s' % self.portal_type, None) \
                                                        and 'nofollow' or 'follow'
            return safe_unicode(result)
        return 'follow'

    @property
    def meta_robots_index(self):
        if self.meta_robots_index_override:
            perseo_property = self.get('meta_robots_index')
            if perseo_property:
                return perseo_property
        override = getattr(self.settings, 'meta_robots_index_override_%s' % self.portal_type, False)  # override?
        if override:
            result = getattr(self.settings, 'meta_robots_index_%s' % self.portal_type, None) \
                                                    and 'noindex' or 'index'
            return safe_unicode(result)
        return 'index'

    @property
    def meta_robots_advanced(self):
        if self.meta_robots_advanced_override:
            perseo_property = self.get('meta_robots_advanced')
            if perseo_property:
                return perseo_property
        override = getattr(self.settings, 'meta_robots_index_override_%s' % self.portal_type, False)  # override?
        if override:
            result = getattr(self.settings, 'meta_robots_advanced_%s' % self.portal_type, ())
            return result
        return ()
