from AccessControl import ClassSecurityInfo
from zope.component import getAdapter, getMultiAdapter
from collective.perseo.interfaces.variables import (IPerseoCompileStringVariables,
                                                    IPerseoCompileStructuredDataStringVariables)
from zope.interface import implements
from Products.CMFPlone.utils import safe_unicode, safe_hasattr

try:
    from App.class_init import InitializeClass
except ImportError:
    from Globals import InitializeClass


class SortedDict(dict):
    """ A sorted dictionary.
    """
    security = ClassSecurityInfo()

    security.declarePublic('items')

    def items(self):
        primary_metatags = self.pmt
        lst = [(name, self[name]) for name in primary_metatags if name in self.keys()] +\
              [(name, self[name]) for name in self.keys() if name not in primary_metatags]
        return lst

    security.declarePublic('__init__')

    def __init__(self, *args, **kwargs):
        super(SortedDict, self).__init__(*args, **kwargs)
        self.pmt = []

    security.declarePublic('__setitem__')

    def __setitem__(self, i, y):
        super(SortedDict, self).__setitem__(i, y)
        if i not in self.pmt:
            self.pmt.append(i)

    security.declarePublic('pop')

    def pop(self, k, *args, **kwargs):
        super(SortedDict, self).pop(k, *args, **kwargs)
        if k in self.pmt:
            self.pmt.remove(k)

try:
    InitializeClass(SortedDict)
except:
    pass


MARKERS = ['%%title%%', '%%tag%%', '%%description%%', '%%startdate%%', '%%enddate%%', '%%sitename%%', '%%fullname%%', '%%searchedtext%%']


class PerseoCompileStringVariables(object):
    implements(IPerseoCompileStringVariables)

    def __init__(self, context):
        self.context = context
        self.portal_state = getMultiAdapter((self.context, self.context.REQUEST),
                                            name=u'plone_portal_state')
        self.context_state = getMultiAdapter((self.context, self.context.REQUEST),
                                             name=u'plone_context_state')

    def get_member_fullname(self, userid):
        member = self.context.portal_membership.getMemberInfo(userid)
        if member:
            return member['fullname'] or userid
        else:
            return userid

    @property
    def data(self):
        result = {}
        result['%%title%%'] = safe_unicode(self.context_state.object_title())
        result['%%sitename%%'] = safe_unicode(self.portal_state.portal_title())
        result['%%description%%'] = self.context.Description()
        result['%%tag%%'] = ', '.join(self.context.Subject())
        if safe_hasattr(self.context, 'Creators'):
            result['%%fullname%%'] = ', '.join([self.get_member_fullname(x) for x in self.context.Creators()])
        else:
            result['%%fullname%%'] = ''
        # we could have event based type with this kind of information
        try:
            result['%%startdate%%'] = self.context.start().strftime('%d-%m-%Y %H:%M')
            result['%%enddate%%'] = self.context.end().strftime('%d-%m-%Y %H:%M')
        except:
            result['%%startdate%%'] = ''
            result['%%enddate%%'] = ''
        return result


class PerseoCompileStringVariablesAuthor(PerseoCompileStringVariables):

    @property
    def data(self):
        result = {}
        result['%%sitename%%'] = safe_unicode(self.portal_state.portal_title())
        path = self.context.REQUEST.get('PATH_INFO', None)
        result['%%fullname%%'] = ''
        if path:
            author = path.split('/')[-1]
            result['%%fullname%%'] = self.get_member_fullname(author)
        return result


class PerseoCompileStringVariablesSearch(PerseoCompileStringVariables):

    @property
    def data(self):
        result = {}
        result['%%sitename%%'] = safe_unicode(self.portal_state.portal_title())
        result['%%searchedtext%%'] = self.context.REQUEST.get('SearchableText', '')
        return result


def compile_variables(context, value, pagetype):
    ad = None
    try:
        ad = getAdapter(context, IPerseoCompileStringVariables, name="perseo_compile_variable_adapter_%s" % pagetype)
    except:
        ad = getAdapter(context, IPerseoCompileStringVariables, name="perseo_compile_variable_adapter_base")

    if not ad:
        return value

    data = ad.data
    for marker in MARKERS:
        if marker in value and marker in data:
            value = value.replace(marker, data[marker])
    return value


class PerseoCompileStructuredDataStringVariables(object):
    implements(IPerseoCompileStructuredDataStringVariables)

    def __init__(self, context):
        self.context = context

    @property
    def data(self):
        result = {
            '%%title%%': self.context.title,
            '%%description%%': self.context.description,
            '%%pubblicationdate%%': self.context.effective_date and self.context.effective_date.strftime('%Y/%m/%d') or '',
            '%%modificationdate%%': self.context.modification_date.strftime('%Y/%m/%d'),
            '%%author%%': self.context.Creator()
            }
        return result


class PerseoCompileStructuredDataStringVariablesNews(PerseoCompileStructuredDataStringVariables):
    implements(IPerseoCompileStructuredDataStringVariables)

    @property
    def data(self):
        superdata = super(PerseoCompileStructuredDataStringVariablesNews, self).data
        superdata['%%imageurl%%'] = self.context.restrictedTraverse('@@images').scale('image', scale='preview').url
        return superdata


class PerseoCompileStructuredDataStringVariablesEvent(PerseoCompileStructuredDataStringVariables):
    implements(IPerseoCompileStructuredDataStringVariables)

    @property
    def data(self):
        superdata = super(PerseoCompileStructuredDataStringVariablesEvent, self).data
        superdata['%%startdate%%'] = self.context.start.strftime('%Y/%m/%d')
        superdata['%%eventurl%%'] = self.context.event_url or self.context.absolute_url()
        superdata['%%address%%'] = self.context.location
        superdata['%%addressname%%'] = self.context.location
        return superdata


STRUCTUREDDATA_MARKERS = ['%%title%%', '%%imageurl%%', '%%pubblicationdate%%', '%%modificationdate%%',
                          '%%author%%', '%%description%%', '%%address%%', '%%eventurl%%', '%%startdate%%',
                          '%%addressname%%']


def compile_structured_data_variables(context, value, pagetype):
    ad = None
    try:
        ad = getAdapter(context,
                        IPerseoCompileStructuredDataStringVariables,
                        name="perseo_compile_structured_data_variables_%s" % pagetype)
    except:
        ad = getAdapter(context,
                        IPerseoCompileStructuredDataStringVariables,
                        name="perseo_compile_structured_data_variables_base")
    if not ad:
        return value

    data = ad.data
    for marker in STRUCTUREDDATA_MARKERS:
        if marker in value and marker in data:
            value = value.replace(marker, data[marker])
    return value
