from zope.interface import implements
from zope import schema

from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from plone.app.users.userdataschema import IUserDataSchemaProvider
from plone.app.users.userdataschema import IUserDataSchema

from collective.perseo import perseoMessageFactory as _


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        ""
        return IEnhancedUserDataSchema


class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """

    facebook_id = schema.TextLine(
        required = False,
        title = _(u'facebook_profile_id',
                  default=u"Facebook profile"),
        description = _(u'help_facebook_profile_id',
                        default=u"This is your facebook profile id / username"),
    )

    twitter_id = schema.TextLine(
        required = False,
        title = _(u'twitter_profile_id',
                  default=u"Twitter profile"),
        description = _(u'help_twitter_profile_id',
                        default=u"This is your twitter username"),
    )

    googleplus_id = schema.TextLine(
        required = False,
        title = _(u'googleplus_profile_id',
                  default=u"Google+ profile"),
        description = _(u'help_googleplus_profile_id',
                        default=u"This is your googleplus profile id"),
    )


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """ """

    def get_facebook_id(self):
        return self.context.getProperty('facebook_id', '')

    def set_facebook_id(self, value):
        return self.context.setMemberProperties({'facebook_id': value})
    facebook_id = property(get_facebook_id, set_facebook_id)

    def get_twitter_id(self):
        return self.context.getProperty('twitter_id', '')

    def set_twitter_id(self, value):
        return self.context.setMemberProperties({'twitter_id': value})
    twitter_id = property(get_twitter_id, set_twitter_id)

    def get_googleplus_id(self):
        return self.context.getProperty('googleplus_id', '')

    def set_googleplus_id(self, value):
        return self.context.setMemberProperties({'googleplus_id': value})
    googleplus_id = property(get_googleplus_id, set_googleplus_id)

