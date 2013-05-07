from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """
    """
    def get_google_author(self):
        return self.context.getProperty('google_author', '')
    def set_google_author(self, value):
        return self.context.setMemberProperties({'google_author': value})
    google_author = property(get_google_author, set_google_author)
