import urllib2

from Products.CMFCore.utils import getToolByName
from zope.component import getUtility
from zope.lifecycleevent import ObjectMovedEvent, ObjectRemovedEvent
from plone.registry.interfaces import IRegistry

from collective.perseo.interfaces import ISEOControlpanel
from collective.perseo.interfaces.settings import ISEOSettings


def include_in_sitemapxml(object):
    """ Returned True if the object is included in sitemap.xml
    """
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISEOControlpanel, check=False)
    not_included_types = settings.not_included_types or []

    return ISEOSettings(object).include_in_sitemap or \
            object.portal_type in not_included_types


def url_open(url):
    """ Perform the url open
    """
    try:
        urllib2.urlopen(url)
    except Exception:
        pass


def PingingObjRemovedFromSiteMapXML(object):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISEOControlpanel, check=False)
    ping_google = settings.ping_google
    ping_bing = settings.ping_bing
    ping_ask = settings.ping_ask

    if (ping_google or ping_bing or ping_ask):
        portal_url = getToolByName(object, 'portal_url')()
        if ping_google:
            url_open("http://www.google.com/webmasters/sitemaps/ping?sitemap=%s/sitemap.xml.gz" % portal_url)
        if ping_bing:
            url_open("http://www.bing.com/webmaster/ping.aspx?siteMap=%s/sitemap.xml.gz" % portal_url)
        if ping_ask:
            url_open("http://submissions.ask.com/ping?sitemap=%s/sitemap.xml.gz" % portal_url)


def Pinging(object):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISEOControlpanel, check=False)
    ping_google = settings.ping_google
    ping_bing = settings.ping_bing
    ping_ask = settings.ping_ask

    if (ping_google or ping_bing or ping_ask) and include_in_sitemapxml(object):
        portal_url = getToolByName(object, 'portal_url')()
        if ping_google:
            url_open("http://www.google.com/webmasters/sitemaps/ping?sitemap=%s/sitemap.xml.gz" % portal_url)
        if ping_bing:
            url_open("http://www.bing.com/webmaster/ping.aspx?siteMap=%s/sitemap.xml.gz" % portal_url)
        if ping_ask:
            url_open("http://submissions.ask.com/ping?sitemap=%s/sitemap.xml.gz" % portal_url)


def event_ObjectUpdated(object, event):
    """ Cases in which the sitemap.xml is modified:
        An object is modified --> The lastmod property of sitemap.xml is changed
        An object has changed its state --> The lastmod property of sitemap.xml is changed
    """
    for desc in getattr(event,'descriptions',[]):
        if type(desc) == type({}) and desc.has_key('included_in_sitemapxml'):
            included_in_sitemapxml = desc.get('included_in_sitemapxml',True)
            if not included_in_sitemapxml:
                # In this case, the user cheks not included in sitemapxml in SEO tab
                # So the object entry is removed from the sitemap.xml
                # and we need to ping without checking if the object is included in the sitemapxml
                PingingObjRemovedFromSiteMapXML(object)

    Pinging(object)


def event_ObjectRemoved(object, event):
    """ Cases in which the sitemap.xml is modified:
        An object is removed --> The entry is removed from the sitemap.xml
    """
    # Delete events can be fired several times for the same object.
    # Some delete event transactions are rolled back.
    # I have to manage it
    if hasattr(object,'REQUEST') and\
       hasattr(object.REQUEST,'form') and\
       (object.REQUEST.form.has_key('form.submitted') and int(object.REQUEST.form.get('form.submitted',0))) or\
       (object.REQUEST.form.has_key('folder_delete')  and object.REQUEST.form.get('folder_delete','')):
        Pinging(object)


def event_ObjectAddedMoved(object, event):
    """ Cases in which the sitemap.xml is modified:
        An object is created --> A new entry is inserted in the sitemap.xml
        An object is copied or moved --> The loc property of sitemap.xml is changed
        An object is renamed --> The loc property of sitemap.xml is changed
    """
    portal_factory = getToolByName(object,'portal_factory')
    if portal_factory.isTemporary(object):
        return

    if hasattr(object,'REQUEST') and\
       hasattr(object.REQUEST,'form') and\
       (object.REQUEST.form.has_key('form.button.save') and object.REQUEST.form.get('form.button.save','')):
        # I'm adding the object

        # Add event can be fired several times
        # Move event can be fired only one time
        # Then I check that the type of event is Move
        if type(event) == ObjectMovedEvent:
            Pinging(object)
    else:
        # I'm pasting the object

        if type(event) != ObjectRemovedEvent:
            Pinging(object)
