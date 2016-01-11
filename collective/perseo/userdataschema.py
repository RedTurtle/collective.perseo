from zope import schema
from zope.interface import implements
from collective.perseo import perseoMessageFactory as _

from pkg_resources import get_distribution

if float(get_distribution('Products.CMFPlone').version) < 5:
    from plone.app.users.userdataschema import IUserDataSchema
    from plone.app.users.userdataschema import IUserDataSchemaProvider
else:
    from plone.app.users.schema import IUserDataSchema
    # XXX fix in a better way. need an iterable
    IUserDataSchemaProvider = tuple()


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):
    google_author = schema.TextLine(
        title=_(u'label_google_author', default=u'Google author'),
        description=_(u'help_google_author',
            default=u"Fill in your google author page, ie. https://plus.google.com/117510669985299383051/"),
        required=False,
        )

    twitter_author = schema.TextLine(
        title=_(u'label_twitter_author', default=u'Twitter author'),
        description=_(u'help_twitter_author',
            default=u"Fill in your twitter author page, ie. @redturtle"),
        required=False,
        )
