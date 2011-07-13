from Acquisition import aq_inner

#from zope.component import queryAdapter
from zope.component import queryMultiAdapter
from plone.app.layout.viewlets.common import ViewletBase

from Products.CMFPlone.utils import safe_unicode, getSiteEncoding

#from collective.perseo.browser.seo_config import ISEOConfigSchema
from collective.perseo.util import SortedDict

# mapping {meta_name:accessor} of all meta tags
METATAGS = {"google-site-verification":"googleWebmasterTools",
            "y_key":"yahooSiteExplorer",
            "msvalidate.01":"bingWebmasterTools"}

METATAGS_ORDER = ["google-site-verification",
                  "y_key",
                  "msvalidate.01"]

class PerSEOMetaTagsViewlet( ViewletBase ):
    """Inserts meta tags in html head of pages"""

    def render(self):
        TEMPLATE = '<meta name="%s" content="%s"/>'
        enc = getSiteEncoding(self.context)
        sfuncd = lambda x, enc=enc:safe_unicode(x, enc)
        return u'\n'.join([TEMPLATE % tuple(map(sfuncd, (k,v))) \
                           for k,v in self.listMetaTags().items()])

    def listMetaTags(self):
        """Calculate list metatags"""

        result = SortedDict()
        #pps = queryMultiAdapter((self.context, self.request), name="plone_portal_state")
        #seo_global = queryAdapter(pps.portal(), ISEOConfigSchema)
        seo_context = queryMultiAdapter((self.context, self.request), name='perseo-context')

        for key in METATAGS_ORDER:
            accessor = METATAGS[key]
            if seo_context._perseo_metatags.has_key(accessor):
                value = seo_context._perseo_metatags.get(accessor, None)
            else:
                method = getattr(seo_context, accessor, None)
                if method is None:
                    method = getattr(aq_inner(self.context).aq_explicit, accessor, None)

                if not callable(method):
                    continue

                # Catch AttributeErrors raised by some AT applications
                try:
                    value = method()
                except AttributeError:
                    value = None

            if not value:
                # No data
                continue
            
            if isinstance(value, (list, tuple)):
                # convert a list to a string
                value = ', '.join(value)

            result[key] = value

        return result