from Acquisition import aq_inner
from DateTime import DateTime
from time import time
from zope.component import queryAdapter
from zope.component import queryMultiAdapter
from zope.schema.interfaces import InvalidValue

from plone.memoize import view, ram

from Products.Archetypes.atapi import DisplayList
from Products.Archetypes.event import ObjectEditedEvent
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.perseo import perseoMessageFactory as _
from collective.perseo.browser.seo_config import ISEOConfigSchema

from zope.annotation.interfaces import IAnnotations
import re
import zope.event



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
            "has_perseo_title":self.has_prop('pSEO_title'),
            "has_perseo_title_config":self.has_perseo_title_config(),
            "perseo_description":self.perseo_description(),
            "has_perseo_description":self.has_prop('pSEO_description'),
            "perseo_keywords":self.perseo_keywords(),
            "has_perseo_keywords": self.has_prop('pSEO_keywords'),
            "perseo_robots_follow":self.perseo_robots_follow(),
            "perseo_robots_index":self.perseo_robots_index(),
            "perseo_robots_advanced":self.perseo_robots_advanced(),
            "has_perseo_robots_advanced":self.has_prop('pSEO_robots_advanced'),
            "perseo_canonical": self.perseo_canonical(),
            "has_perseo_canonical": self.has_prop('pSEO_canonical'),
            "perseo_included_in_sitemapxml": self.perseo_included_in_sitemapxml(),
            "perseo_priority_sitemapxml": self.perseo_priority_sitemapxml(),
            "perseo_itemtype":self.perseo_itemtype(),
            "has_perseo_itemtype":self.has_prop('pSEO_itemtype'),
            "has_perseo_robots_follow":self.has_prop('pSEO_robots_follow'),
            "has_perseo_robots_index":self.has_prop('pSEO_robots_index'),
            "has_perseo_included_in_sitemapxml":self.has_prop('pSEO_included_in_sitemapxml'),
            }
        return perseo_metatags
    
    def has_prop(self,property):
        try:
            return IAnnotations(self.context).has_key(property)
        except:
            return None
    
    def perseo_itemtype(self):
        return self.getPerSEOProperty('pSEO_itemtype', default='http://schema.org/WebPage')
    
    def perseo_priority_sitemapxml(self):
        return self.getPerSEOProperty('pSEO_priority_sitemapxml', default=None)
        
    def perseo_included_types(self):
        if self.gseo:
            return getattr(self.gseo, 'not_included_types', ())
        return ()
    
    def getYesNoOptions(self):
        """Get a sample vocabulary
        """
        return DisplayList((("yes", _(u"Yes"),),
                            ("no", _(u"No"),),
                            ))
    
    def perseo_included_in_sitemapxml(self):
        context = aq_inner(self.context)
        included_types = self.perseo_included_types()
        
        default = context.portal_type in included_types
        
        return self.getPerSEOProperty('pSEO_included_in_sitemapxml', default=default)
    
    def perseo_canonical(self):
        return self.getPerSEOProperty('pSEO_canonical', default=self.context.absolute_url())
    
    def getRobotsAdvanced(self):
        """Get a sample vocabulary for Robots Advanced options
        """
        return DisplayList((("", _(u"None"),),
                            ("noodp", _(u"NO ODP"),),
                            ("noydir", _(u"NO YDIR"),),
                            ("noarchive", _(u"No Archive"),),
                            ("nosnippet", _(u"No Snippet"),),
                            ))
    
    def perseo_robots_follow(self):
        return self.getPerSEOProperty('pSEO_robots_follow',default='follow')
    
    def perseo_robots_index(self):
        return self.getPerSEOProperty('pSEO_robots_index',default='index')
    
    def perseo_robots_advanced(self):
        default = []
        for key in self.getRobotsAdvanced().keys():
            if self.get_gseo_field('robots_%s' % key):
                default.append(key)
        return self.getPerSEOProperty('pSEO_robots_advanced',default=default)
    
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
        
#        if perseo_robots:
#            return (', '.join(perseo_robots),) + self._perseo_metatags["perseo_robots_advanced"]
#        else:
#            return self._perseo_metatags["perseo_robots_advanced"]
    
    def getPerSEOProperty( self, property_name, accessor='', default=None ):
        """ Get value from seo property by property name.
        """
        context = aq_inner(self.context)
        
        try:
            annotations = IAnnotations(context)

            if annotations.has_key(property_name):
                return annotations.get(property_name, default)
        except:
            return default
        
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
    
    def perseo_itemscope_itemtype( self ):
        """ Returned itemscope_itemtype_attrs_enable from Plone SEO Configuration Control Panel Tool
        """
        result = False
        if self.gseo:
            result = self.gseo.itemscope_itemtype_attrs_enable
        return result
    
    def perseo_indexing_feed_rss( self ):
        """ Returned indexing_feed_rss from Plone SEO Configuration Control Panel Tool
        """
        result = False
        if self.gseo:
            result = self.gseo.indexing_feed_rss
        return result

class PerSEOContextPloneSiteRoot(PerSEOContext):
    """ Calculate html header meta tags on context. Context == PloneSiteRoot
    """
    
    def perseo_robots_what_page(self):
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
        
    def perseo_robots_follow(self):
        page = self.perseo_robots_what_page()
        if page:
            gseo_field = self.get_gseo_field('indexing_%s' % page)
            if gseo_field:
                return 'nofollow'
        else:
            perseo_property = self.getPerSEOProperty('pSEO_robots_follow')
            if perseo_property:
                return perseo_property
        
        return 'follow'
    
    def perseo_robots_index(self):
        page = self.perseo_robots_what_page()
        if page:
            gseo_field = self.get_gseo_field('indexing_%s' % page)
            if gseo_field:
                return 'noindex'
        else:
            perseo_property = self.getPerSEOProperty('pSEO_robots_index')
            if perseo_property:
                return perseo_property
        
        return 'index'
    
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
            try:
                self.context.restrictedTraverse(self.request.PATH_INFO)
            except:
                return 'notfoundpage'
            return 'homepage'

    def perseo_title( self ):
        page = self.perseo_what_page()
        if page == 'homepage':
            perseo_property = self.getPerSEOProperty( 'pSEO_title' )
            if perseo_property:
                return perseo_property

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
        page = self.perseo_what_page()
        if page == 'homepage':
            perseo_property = self.getPerSEOProperty( 'pSEO_description' )
            if perseo_property:
                return perseo_property
        
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
        page = self.perseo_what_page()
        if page == 'homepage':
            perseo_property = self.getPerSEOProperty( 'pSEO_keywords' )
            if perseo_property:
                return perseo_property
        
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

    def perseo_robots_follow(self):
        perseo_property = self.getPerSEOProperty('pSEO_robots_follow')
        if perseo_property:
            return perseo_property
        
        gseo_field = self.get_gseo_field('indexing_page')
        if gseo_field:
            return 'nofollow'
        
        return 'follow'
    
    def perseo_robots_index(self):
        perseo_property = self.getPerSEOProperty('pSEO_robots_index')
        if perseo_property:
            return perseo_property
        
        gseo_field = self.get_gseo_field('indexing_page')
        if gseo_field:
            return 'noindex'
        
        return 'index'
    
    def perseo_what_page( self ):
        
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
        
    def perseo_title( self ):
        perseo_property = self.getPerSEOProperty( 'pSEO_title' )
        if perseo_property:
            return perseo_property
        
        try:
            self.context.restrictedTraverse(self.request.PATH_INFO)
        except:
            gseo_field = self.perseo_variables(self.get_gseo_field('notfoundpage_title'))
            if gseo_field:
                return gseo_field
        
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_title' % self.portal_type))
        if gseo_field:
            return gseo_field
        
        return self.pcs.object_title()
    
    def has_perseo_title_config( self ):
        
        try:
            self.context.restrictedTraverse(self.request.PATH_INFO)
        except:
            gseo_field = self.perseo_variables(self.get_gseo_field('notfoundpage_title'))
            if gseo_field:
                return True
            else:
                return False
        
        gseo_field = self.perseo_variables(self.get_gseo_field('%s_title' % self.portal_type))
        if gseo_field:
            return True
        else:
            return False
        
    def perseo_description( self ):
        perseo_property = self.getPerSEOProperty( 'pSEO_description' )
        if perseo_property:
            return perseo_property
        
        try:
            self.context.restrictedTraverse(self.request.PATH_INFO)
        except:
            gseo_field = self.perseo_variables(self.get_gseo_field('notfoundpage_description'))
            if gseo_field:
                return gseo_field
        
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
        
        try:
            self.context.restrictedTraverse(self.request.PATH_INFO)
        except:
            gseo_field = self.perseo_variables(self.get_gseo_field('notfoundpage_keywords'))
            if gseo_field:
                return gseo_field
        
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
        
    def setProperty(self, property, value):
        """ Add a new item to annotation.

            Sets a new item with the given key, value or changes it.
        """
        state = False
        context = aq_inner(self.context)
        annotations = IAnnotations(context)
        if annotations.has_key(property):
            current_value = annotations.get(property, None)
            if value != current_value:
                state = True
            annotations[property] = value
            if (property == 'pSEO_included_in_sitemapxml' or property == 'pSEO_priority_sitemapxml')\
                and state:
                context.reindexObject(idxs=[])
        else:
            state = True
            annotations[property] = value
        
        return state
    
    def delProperties(self, delete_list):
        """ Delete some items to annotation.
        """
        context = aq_inner(self.context)
        annotations = IAnnotations(context)
        for property in delete_list:
            annotations.pop(property)
        
    def manageSEOProps(self, **kw):
        """ Manage seo properties.
        """
        description = {}
        state = False
        context = aq_inner(self.context)
        annotations = IAnnotations(context)
        
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
                if perseo_value:
                    if perseo_key == "robots_advanced" and '' in perseo_value:
                        perseo_value.remove('')
                    if perseo_key=="included_in_sitemapxml":
                        if perseo_value == 'no':
                            perseo_value = False
                        else:
                            perseo_value = True
                if perseo_key=="priority_sitemapxml":
                    if perseo_value == '' and not annotations.has_key(PROP_PREFIX+perseo_key):
                        continue
                    perseo_value = perseo_value and float(perseo_value) or perseo_value
                if self.setProperty(PROP_PREFIX+perseo_key, perseo_value):
                    state = True
                    if perseo_key == 'included_in_sitemapxml' or perseo_key == 'priority_sitemapxml':
                        description[perseo_key] = perseo_value
            elif annotations.has_key(PROP_PREFIX+perseo_key):
                delete_list.append(PROP_PREFIX+perseo_key)
        if delete_list:
            state = True
            self.delProperties(delete_list)
        
        if description:
            # Cases in which the sitemap.xml is modified:
            # pSEO_included_in_sitemapxml property is updated --> A new entry is inserted/removed in the sitemap.xml
            # pSEO_priority_sitemapxml property is updated --> The priority property of sitemap.xml is changed
            event = ObjectEditedEvent(context, description)
            zope.event.notify(event)
        
        return state
    
    def canonical_validate(self, value):
        # non space and no new line(should be pickier)
        _is_canonical = re.compile(r"\S*$").match
        
        if not _is_canonical(value):
            raise InvalidValue(value)
    
    def validate(self,form):
        msg = []
        if form.has_key(PERSEO_PREFIX+'canonical') \
            and form.has_key(PERSEO_PREFIX+'canonical'+SUFFIX)\
            and form.get(PERSEO_PREFIX+'canonical'+SUFFIX):
            canonical_url = form.get(PERSEO_PREFIX+'canonical')
            try:
                self.canonical_validate(canonical_url)
            except InvalidValue, e:
                msg.append(_(u"wrong_canonical_url", 
                             default=u'The Canonical URL "${url}" is incorrect',
                             mapping={'url':str(e)}))
        if form.has_key(PERSEO_PREFIX+'priority_sitemapxml')\
            and form.get(PERSEO_PREFIX+'priority_sitemapxml'):
            priority_sitemapxml = form.get(PERSEO_PREFIX+'priority_sitemapxml')
            try:
                priority_sitemapxml = float(priority_sitemapxml)
                if priority_sitemapxml < 0.1:
                    msg.append(_(u"wrong_priority_sitemapxml_greater", 
                                 default=u"The Priority sitemap.xml.gz need to be greater than 0.0"))
                if priority_sitemapxml > 1.0:
                    msg.append(_(u"wrong_priority_sitemapxml_less", 
                                 default=u"The Priority sitemap.xml.gz need to be less than or equal to 1.0"))
            except ValueError, e:
                msg.append(_(u"wrong_priority_sitemapxml", 
                             default=u"The Priority sitemap.xml.gz must be a number"))
        return msg

    def __call__( self ):
        """ Perform the update SEO properties and redirect if necessary,
            or render the template.
        """
        request = self.request
        form = request.form
        
        portal_properties = getToolByName(self.context, 'portal_properties')
        use_view_action = portal_properties.site_properties.typesUseViewActionInListings
        item_type = self.context.portal_type
        item_url = self.context.absolute_url()
        redirect_url = item_type in use_view_action and item_url+'/view' or item_url
        
        if form.get('form.button.Cancel', False):
            return request.response.redirect(redirect_url)
        
        if form.get('form.button.Save', False):
            context = aq_inner(self.context)
            msgs = self.validate(form)
            if msgs:
                for msg in msgs:
                    context.plone_utils.addPortalMessage(msg, 'error')
                return self.template()
            state = self.manageSEOProps(**form)
            if state:
                state = _('perseo_settings_saved', default=u'The SEO settings have been saved.')
                context.plone_utils.addPortalMessage(state)
                kwargs = {'modification_date' : DateTime()}
                context.plone_utils.contentEdit(context, **kwargs)
            return request.response.redirect(redirect_url)
        
        return self.template()
