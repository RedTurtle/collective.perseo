from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.social.like.browser.viewlets import SocialMetadataViewlet as BaseLikeViewlet


class SocialMetadataViewlet(BaseLikeViewlet):
    """Customize the metadata viewlet
    """
    render = ViewPageTemplateFile("metadata.pt")
