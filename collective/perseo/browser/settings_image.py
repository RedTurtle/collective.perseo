from collective.perseo.browser.settings_at import ATSeoContextAdapter


class ImageSeoContextAdapter(ATSeoContextAdapter):

    @property
    def og_image(self):
        return self.get('og_image') or self.context.absolute_url()

    @property
    def twitter_card(self):
        return self.get('twitter_card') or 'photo'
