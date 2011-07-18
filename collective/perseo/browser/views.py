from Acquisition import aq_inner
from DateTime import DateTime
from time import time
from zope.component import queryAdapter
from zope.component import queryMultiAdapter

from plone.memoize import view, ram

from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.perseo import perseoMessageFactory as _
from collective.perseo.browser.seo_config import ISEOConfigSchema

PERSEO_PREFIX = 'perseo_'
SUFFIX = '_override'
PROP_PREFIX = 'pSEO_'

# Ram cache function, which depends on plone instance and time
def plone_instance_time(method, self, *args, **kwargs):
    return (self.pps.portal(), time() // (60 * 60))

class PerSEOContext(BrowserView):
    """ Calculate html header meta tags on context.
    """

    def __init__(self, *args, **kwargs):
        super(PerSEOContext, self).__init__(*args, **kwargs)
        self.pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        self.pcs = queryMultiAdapter((self.context, self.request), name="plone_context_state")
        self.gseo = queryAdapter(self.pps.portal(), ISEOConfigSchema)
        self._perseo_metatags = self._getPerSEOMetaTags()

    def __getitem__(self, key):
        return self._perseo_metatags.get(key, '')
    
    @view.memoize
    def _getPerSEOMetaTags(self):
        perseo_metatags = {
            "googleWebmasterTools": self.seo_globalGoogleWebmasterTools(),
            "yahooSiteExplorer": self.seo_globalYahooSiteExplorer(),
            "bingWebmasterTools":self.seo_globalBingWebmasterTools(),
            "perseo_title":self.perseo_title(),
            "has_perseo_title":self.context.hasProperty('pSEO_title'),
            "has_perseo_title_config":self.has_perseo_title_config(),
            "perseo_description":self.perseo_description(),
            "has_perseo_description":self.context.hasProperty('pSEO_description'),
            "perseo_keywords":self.perseo_keywords(),
            "has_perseo_keywords":self.context.hasProperty('pSEO_keywords'),
            }
        return perseo_metatags
    
    def getPerSEOProperty( self, property_name, accessor='', default=None ):
        """ Get value from seo property by property name.
        """
        context = aq_inner(self.context)

        if context.hasProperty(property_name):
            return context.getProperty(property_name, default)
        
        if accessor:
            method = getattr(context, accessor, default)
            if not callable(method):
                return default

            # Catch AttributeErrors raised by some AT applications
            try:
                value = method()
            except AttributeError:
                value = default

            return value
        
        return default
    
    @ram.cache(plone_instance_time)
    def seo_globalGoogleWebmasterTools( self ):
        """ Returned Google Webmaster Tools from Plone SEO Configuration Control Panel Tool
        """
        result = ''
        if self.gseo:
            result = self.gseo.googleWebmasterTools
        return result
    
    @ram.cache(plone_instance_time)
    def seo_globalYahooSiteExplorer( self ):
        """ Returned Yahoo Site Explorer from Plone SEO Configuration Control Panel Tool
        """
        result = ''
        if self.gseo:
            result = self.gseo.yahooSiteExplorer
        return result
    
    @ram.cache(plone_instance_time)
    def seo_globalBingWebmasterTools( self ):
        """ Returned Bing Webmaster Tools from Plone SEO Configuration Control Panel Tool
        """
        result = ''
        if self.gseo:
            result = self.gseo.bingWebmasterTools
        return result
    
    def get_gseo_field( self, field ):
        """ Returned field from Plone SEO Configuration Control Panel Tool
        """
        result = None
        if self.gseo:
            result = getattr(self.gseo, field, None)
        return result
    
    def perseo_title( self ):
        return self.getPerSEOProperty( 'pSEO_title', default=self.pcs.object_title() )
    
    def has_perseo_title_config( self ):
        return False
    
    def perseo_description( self ):
        return self.getPerSEOProperty( 'pSEO_description', accessor='Description' )
    
    def perseo_keywords( self ):
        return self.getPerSEOProperty( 'pSEO_keywords', 'Subject', () )
    
    def perseo_variables(self, value):
        if value:
            if isinstance(value, (list, tuple)):
                new_value = []
                for x in value:
                    new_value.append(safe_unicode(x.replace('%%title%%',self.pcs.context.Title()).\
                                                    replace('%%tag%%',' '.join(self.pcs.context.Subject()))))
                return new_value
            return safe_unicode(value.replace('%%title%%',self.pcs.context.Title()).\
                                    replace('%%tag%%',' '.join(self.pcs.context.Subject())))
        return value

class PerSEOContextPloneSiteRoot(PerSEOContext):
    """ Calculate html header meta tags on context. Context == PloneSiteRoot
    """
    
    def perseo_what_page(self):
        # I take template_id as is done in ploneview
        # if all goes well for ploneview is fine in my general view
        template_id = None
        if 'PUBLISHED' in self.request:
            if getattr(self.request['PUBLISHED'], 'getId', None):
                # template inside skins   
                template_id = self.request['PUBLISHED'].getId()
            if getattr(self.request['PUBLISHED'], __name__, None):
                # template inside browser view
                template_id = self.request['PUBLISHED'].__name__
        
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
            return 'homepage'

    def perseo_title( self ):
        perseo_property = self.getPerSEOProperty( 'pSEO_title' )
        if perseo_property:
            return perseo_property

        page = self.perseo_what_page()
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_title' % page))
        if gseo_field:
            return gseo_field
        
        return self.pcs.object_title()
    
    def has_perseo_title_config( self ):
        page = self.perseo_what_page()
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_title' % page))
        if gseo_field:
            return True
        else:
            return False
    
    def perseo_description( self ):
        perseo_property = self.getPerSEOProperty( 'pSEO_description' )
        if perseo_property:
            return perseo_property
        
        page = self.perseo_what_page()
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_description' % page))
        if gseo_field:
            return gseo_field
        
        context = aq_inner(self.context)
        try:
            value = context.Description()
        except AttributeError:
            value = None
        return value
    
    def perseo_keywords( self ):
        perseo_property = self.getPerSEOProperty( 'pSEO_keywords' )
        if perseo_property:
            return perseo_property
        
        page = self.perseo_what_page()
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_keywords' % page))
        if gseo_field:
            return gseo_field
        
        context = aq_inner(self.context)
        try:
            value = context.Subject()
        except AttributeError:
            value = ()
        return value
            
class PerSEOContextATDocument(PerSEOContext):
    """ Calculate html header meta tags on context. Context == ATDocument
    """
    def perseo_what_page( self ):
        context = self.pcs.context
        parent = self.pcs.parent()
        
        if parent == self.pps.portal() and parent.getDefaultPage() == context.id:
            # this document is the home page
            return 'homepage'
        else:
            return 'singlepage'
        
    def perseo_title( self ):
        perseo_property = self.getPerSEOProperty( 'pSEO_title' )
        if perseo_property:
            return perseo_property
        
        page = self.perseo_what_page()
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_title' % page))
        if gseo_field:
            return gseo_field
        
        return self.pcs.object_title()
    
    def has_perseo_title_config( self ):
        page = self.perseo_what_page()
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_title' % page))
        if gseo_field:
            return True
        else:
            return False
    
    def perseo_description( self ):
        perseo_property = self.getPerSEOProperty( 'pSEO_description' )
        if perseo_property:
            return perseo_property
        
        page = self.perseo_what_page()
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_description' % page))
        if gseo_field:
            return gseo_field
        
        context = aq_inner(self.context)
        try:
            value = context.Description()
        except AttributeError:
            value = None
        return value
    
    def perseo_keywords( self ):
        perseo_property = self.getPerSEOProperty( 'pSEO_keywords' )
        if perseo_property:
            return perseo_property
        
        page = self.perseo_what_page()
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_keywords' % page))
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
    portal_type = ''
        
    def perseo_title( self ):
        perseo_property = self.getPerSEOProperty( 'pSEO_title' )
        if perseo_property:
            return perseo_property
        
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_title' % self.portal_type))
        if gseo_field:
            return gseo_field
        
        return self.pcs.object_title()
    
    def has_perseo_title_config( self ):
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_title' % self.portal_type))
        if gseo_field:
            return True
        else:
            return False
        
    def perseo_description( self ):
        perseo_property = self.getPerSEOProperty( 'pSEO_description' )
        if perseo_property:
            return perseo_property
        
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_description' % self.portal_type))
        if gseo_field:
            return gseo_field
        
        context = aq_inner(self.context)
        try:
            value = context.Description()
        except AttributeError:
            value = None
        return value
    
    def perseo_keywords( self ):
        perseo_property = self.getPerSEOProperty( 'pSEO_keywords' )
        if perseo_property:
            return perseo_property
        
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_keywords' % self.portal_type))
        if gseo_field:
            return gseo_field
        
        context = aq_inner(self.context)
        try:
            value = context.Subject()
        except AttributeError:
            value = ()
        return value
    
class PerSEOContextATEvent(PerSEOContextPortalTypes):
    """ Calculate html header meta tags on context. Context == ATEvent
    """
    portal_type = 'event'
    
class PerSEOContextATFile(PerSEOContextPortalTypes):
    """ Calculate html header meta tags on context. Context == ATFile
    """
    portal_type = 'file'
    
class PerSEOContextATFolder(PerSEOContextPortalTypes):
    """ Calculate html header meta tags on context. Context == ATFolder
    """
    portal_type = 'folder'
    
class PerSEOContextATImage(PerSEOContextPortalTypes):
    """ Calculate html header meta tags on context. Context == ATImage
    """
    portal_type = 'image'
    
class PerSEOContextATLink(PerSEOContextPortalTypes):
    """ Calculate html header meta tags on context. Context == ATLink
    """
    portal_type = 'link'
    
class PerSEOContextATNewsItem(PerSEOContextPortalTypes):
    """ Calculate html header meta tags on context. Context == ATNewsItem
    """
    portal_type = 'newsItem'
    
class PerSEOContextATTopic(PerSEOContextPortalTypes):
    """ Calculate html header meta tags on context. Context == ATTopic
    """
    portal_type = 'topic'

class PerseoTabAvailable(BrowserView):
    """"""

    def checkPerseoTabAvailable(self):
        """ Checks visibility of SEO tab for context
        """
        return True
    
class PerSEOTabContext( BrowserView ):
    """ This class contains methods that allows to manage SEO tab.
    """
    template = ViewPageTemplateFile('templates/perseo_tab_context.pt')

    def __init__(self, *args, **kwargs):
        super(PerSEOTabContext, self).__init__(*args, **kwargs)
        self.pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        self.gseo = queryAdapter(self.pps.portal(), ISEOConfigSchema)
        
    def setProperty(self, property, value, type='string'):
        """ Add a new property.

            Sets a new property with the given id, value and type or changes it.
        """
        context = aq_inner(self.context)
        if context.hasProperty(property):
            context.manage_changeProperties({property: value})
        else:
            context.manage_addProperty(property, value, type)
        
    def manageSEOProps(self, **kw):
        """ Manage seo properties.
        """
        state = False
        context = aq_inner(self.context)
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
                t_value = 'string'
                if type(perseo_value)==type([]) or type(perseo_value)==type(()): t_value = 'lines'
                self.setProperty(PROP_PREFIX+perseo_key, perseo_value, type=t_value)
                state = True
            elif context.hasProperty(PROP_PREFIX+perseo_key):
                delete_list.append(PROP_PREFIX+perseo_key)
        if delete_list:
            context.manage_delProperties(delete_list)
            state = True
        return state

    def __call__( self ):
        """ Perform the update SEO properties and redirect if necessary,
            or render the template.
        """
        request = self.request
        form = request.form
        
        if form.get('form.button.Cancel', False):
            return request.response.redirect(self.context.absolute_url())
        
        if form.get('form.button.Save', False):
            state = self.manageSEOProps(**form)
            if state:
                context = aq_inner(self.context)
                state = _('perseo_settings_saved', default=u'The SEO settings have been saved.')
                context.plone_utils.addPortalMessage(state)
                kwargs = {'modification_date' : DateTime()}
                context.plone_utils.contentEdit(context, **kwargs)
            return request.response.redirect(self.context.absolute_url())
        
        return self.template()
