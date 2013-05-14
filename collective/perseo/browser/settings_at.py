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
        if not self.meta_robots_follow_override:
            return 'follow'
        perseo_property = self.get('meta_robots_follow')
        if perseo_property:
            return perseo_property
        return getattr(self.settings, 'indexing_%s' % self.portal_type) \
                                                    and 'nofollow' or 'follow'

    @property
    def meta_robots_index(self):
        if not self.meta_robots_index_override:
            return 'index'
        perseo_property = self.get('meta_robots_index')
        if perseo_property:
            return perseo_property
        return getattr(self.settings, 'indexing_%s' % self.portal_type) \
                                                    and 'noindex' or 'index'
