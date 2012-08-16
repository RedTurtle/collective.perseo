from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.perseo.browser.seo_context import PerSEOContextPortalTypes


class PerSEOContextLeadImageable(PerSEOContextPortalTypes):

    def perseo_image(self):
        clfield = self.context.getField(IMAGE_FIELD_NAME)
        if clfield is not None:
            value = clfield.get(self.context)
            if value:
                return '%s/leadImage_preview' % self.context.absolute_url()

        return super(PerSEOContextLeadImageable, self).perseo_image()

