from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope import schema
from zope.interface import implements
from collective.perseo import perseoMessageFactory as _


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
