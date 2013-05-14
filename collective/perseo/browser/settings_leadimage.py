from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.interfaces import ILeadImageable
from collective.perseo.browser.settings_at import ATSeoContextAdapter


class LeadImageSeoContextAdapter(ATSeoContextAdapter):

    @property
    def og_image(self):
        default = super(LeadImageSeoContextAdapter, self).og_image

        if not ILeadImageable.providedBy(self.context):
            return default

        field = self.context.getField(IMAGE_FIELD_NAME)
        if not field:
            return default

        value = field.get(self.context)
        if not value:
            return default

        return self.get('og_image') or \
                '%s/leadImage_preview' % self.context.absolute_url()
