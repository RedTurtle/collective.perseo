from zope import schema
from zope.interface import implementer
from collective.perseo import perseoMessageFactory as _

#if float(get_distribution('Products.CMFPlone').version) < 5:
#    from plone.app.users.userdataschema import IUserDataSchema
#    from plone.app.users.userdataschema import IUserDataSchemaProvider
#else:
#    from plone.app.users.schema import IUserDataSchema
# XXX fix in a better way. need an iterable
#    IUserDataSchemaProvider = tuple()
try:
    from plone.app.users.schema import IUserDataSchema
except:
    from plone.app.users.userdataschema import IUserDataSchema

#XXX fix in a better way. need an iterable
IUserDataSchemaProvider = tuple()

@implementer(IUserDataSchemaProvider)
class UserDataSchemaProvider(object):

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
