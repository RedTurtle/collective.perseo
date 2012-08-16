from Acquisition import aq_inner
from Products.Archetypes.interfaces.field import IImageField
from collective.perseo.browser.views import PerSEOGenericContext


class PerSEOContext(PerSEOGenericContext):
    """ Calculate html header meta tags on context.
    """

    def perseo_itemtype(self):
        return self.getPerSEOProperty('pSEO_itemtype', default='http://schema.org/WebPage')

    def perseo_priority_sitemapxml(self):
        return self.getPerSEOProperty('pSEO_priority_sitemapxml', default=None)

    def perseo_included_types(self):
        if self.gseo:
            return getattr(self.gseo, 'not_included_types', ())
        return ()

    def perseo_included_in_sitemapxml(self):
        context = aq_inner(self.context)
        included_types = self.perseo_included_types()
        default = context.portal_type in included_types
        return self.getPerSEOProperty('pSEO_included_in_sitemapxml', default=default)

    def perseo_canonical(self):
        return self.getPerSEOProperty('pSEO_canonical', default=self.context.absolute_url())

    def perseo_robots_follow(self):
        return self.getPerSEOProperty('pSEO_robots_follow', default='follow')

    def perseo_robots_index(self):
        return self.getPerSEOProperty('pSEO_robots_index', default='index')

    def perseo_robots_advanced(self):
        default = []
        for key in self.getRobotsAdvanced().keys():
            if self.get_gseo_field('robots_%s' % key):
                default.append(key)
        return self.getPerSEOProperty('pSEO_robots_advanced', default=default)

    def perseo_robots(self):
        perseo_robots = []

        if self._perseo_metatags["perseo_robots_index"]:
            perseo_robots.append(self._perseo_metatags["perseo_robots_index"])
        if self._perseo_metatags["perseo_robots_follow"]:
            perseo_robots.append(self._perseo_metatags["perseo_robots_follow"])

        if self._perseo_metatags["perseo_robots_index"] == 'noindex' \
            and not self._perseo_metatags["perseo_robots_follow"]:
            perseo_robots.append('nofollow')

        return perseo_robots + list(self._perseo_metatags["perseo_robots_advanced"])

    def perseo_title(self):
        return self.getPerSEOProperty('pSEO_title', default=self.pcs.object_title())

    def has_perseo_title_config(self):
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_title' % self.unified_template_id))
        if gseo_field:
            return True
        else:
            return False

    def perseo_description(self):
        return self.getPerSEOProperty('pSEO_description', accessor='Description')

    def perseo_keywords(self):
        return self.getPerSEOProperty( 'pSEO_keywords', 'Subject', () )

    def perseo_itemscope_itemtype(self):
        """ Returned itemscope_itemtype_attrs_enable from Plone SEO Configuration Control Panel Tool
        """
        result = False
        if self.gseo:
            result = self.gseo.itemscope_itemtype_attrs_enable
        return result

    def perseo_indexing_feed_rss(self):
        """ Returned indexing_feed_rss from Plone SEO Configuration Control Panel Tool
        """
        result = False
        if self.gseo:
            result = self.gseo.indexing_feed_rss
        return result

    def perseo_image(self):
        return '%s/logo.png' % self.context.portal_url()

    def twitter_card_type(self):
        return 'summary'

    def facebook_metatype(self):
        return 'website'


class PerSEOContextPloneSiteRoot(PerSEOContext):
    """ Calculate html header meta tags on context. Context == PloneSiteRoot
    """

    def perseo_robots_follow(self):
        gseo_field = self.get_gseo_field('indexing_%s' % self.unified_template_id)
        if gseo_field:
            return 'nofollow'

        perseo_property = self.getPerSEOProperty('pSEO_robots_follow')
        if perseo_property:
            return perseo_property

        return 'follow'

    def perseo_robots_index(self):
        gseo_field = self.get_gseo_field('indexing_%s' % self.unified_template_id)
        if gseo_field:
            return 'noindex'

        perseo_property = self.getPerSEOProperty('pSEO_robots_index')
        if perseo_property:
            return perseo_property

        return 'index'

    def perseo_title( self ):
        if self.unified_template_id == 'homepage':
            perseo_property = self.getPerSEOProperty('pSEO_title')
            if perseo_property:
                return perseo_property

        gseo_field = self.perseo_variables(self.get_gseo_field('%s_title' % self.unified_template_id))
        if gseo_field:
            return gseo_field

        return self.pcs.object_title()

    def perseo_description( self ):
        if self.unified_template_id == 'homepage':
            perseo_property = self.getPerSEOProperty('pSEO_description')
            if perseo_property:
                return perseo_property

        gseo_field = self.perseo_variables(self.get_gseo_field('%s_description' % self.unified_template_id))
        if gseo_field:
            return gseo_field

        context = aq_inner(self.context)
        try:
            value = context.Description()
        except AttributeError:
            value = None
        return value

    def perseo_keywords( self ):
        if self.unified_template_id == 'homepage':
            perseo_property = self.getPerSEOProperty('pSEO_keywords')
            if perseo_property:
                return perseo_property

        gseo_field = self.perseo_variables(self.get_gseo_field('%s_keywords' % self.unified_template_id))
        if gseo_field:
            return gseo_field

        context = aq_inner(self.context)
        try:
            value = context.Subject()
        except AttributeError:
            value = ()
        return value


class PerSEOContextPortalTypes(PerSEOContext):
    """ Calculate html header meta tags on context. Context == a portal type
    """

    @property
    def portal_type(self):
        return self.context.portal_type.lower().replace(' ','')

    @property
    def unified_template_id(self):
        try:
            self.context.restrictedTraverse(self.request.PATH_INFO)
        except:
            return 'notfoundpage'

        context = self.pcs.context
        parent = self.pcs.parent()

        if parent == self.pps.portal() and parent.getDefaultPage() == context.id:
            # this document is the home page
            return 'homepage'
        else:
            return self.portal_type

    def perseo_robots_follow(self):
        perseo_property = self.getPerSEOProperty('pSEO_robots_follow')
        if perseo_property:
            return perseo_property

        gseo_field = self.get_gseo_field('indexing_%s' % self.portal_type)
        if gseo_field:
            return 'nofollow'

        return 'follow'

    def perseo_robots_index(self):
        perseo_property = self.getPerSEOProperty('pSEO_robots_index')
        if perseo_property:
            return perseo_property

        gseo_field = self.get_gseo_field('indexing_%s' % self.portal_type)
        if gseo_field:
            return 'noindex'

        return 'index'

    def perseo_title(self):
        perseo_property = self.getPerSEOProperty('pSEO_title')
        if perseo_property:
            return perseo_property

        gseo_field = self.perseo_variables(self.get_gseo_field('%s_title' % self.unified_template_id))
        if gseo_field:
            return gseo_field

        return self.pcs.object_title()

    def perseo_description(self):
        perseo_property = self.getPerSEOProperty('pSEO_description')
        if perseo_property:
            return perseo_property

        gseo_field = self.perseo_variables(self.get_gseo_field('%s_description' % self.unified_template_id))
        if gseo_field:
            return gseo_field

        context = aq_inner(self.context)
        try:
            value = context.Description()
        except AttributeError:
            value = None
        return value

    def perseo_keywords( self ):
        perseo_property = self.getPerSEOProperty('pSEO_keywords')
        if perseo_property:
            return perseo_property

        gseo_field = self.perseo_variables(self.get_gseo_field('%s_keywords' % self.unified_template_id))
        if gseo_field:
            return gseo_field

        context = aq_inner(self.context)
        try:
            value = context.Subject()
        except AttributeError:
            value = ()
        return value

    def perseo_image(self):
        for field in self.context.Schema().fields():
            if IImageField.providedBy(field):
                if 'preview' in field.getAvailableSizes(self.context):  # Smaller then preview is not accepated
                    return '%s/%s_preview' % (self.context.absolute_url(), field.__name__)
        return super(PerSEOContextPortalTypes, self).perseo_image()


class PerSEOContextIImage(PerSEOContextPortalTypes):
    """ Calculate html header meta tags on context. Context == IImage
    """

    def twitter_card_type(self):
        return 'photo'

