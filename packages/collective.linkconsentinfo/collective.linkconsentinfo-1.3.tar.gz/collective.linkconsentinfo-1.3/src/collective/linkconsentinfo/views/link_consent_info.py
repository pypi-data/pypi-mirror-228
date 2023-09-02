# -*- coding: utf-8 -*-

from collective.linkconsentinfo.controlpanels.link_consent_info import (
    ILinkConsentInfoControlPanel,
)
from plone.app.contenttypes.browser.link_redirect_view import (
    LinkRedirectView,
    NON_REDIRECTABLE_URL_SCHEMES,
)
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import ITypesSchema
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getUtility

import six


class LinkConsentInfo(LinkRedirectView):
    """ Subclass LinkRedirectView to inject link consent switch and template
    """

    def __call__(self):
        """Redirect to the Link target URL, if and only if:
         - redirect_links property is enabled in
           configuration registry
         - the link is of a redirectable type (no mailto:, etc)
         - enable_consent_info is False
         - AND current user doesn't have permission to edit the Link"""

        context = self.context
        mtool = getToolByName(context, "portal_membership")

        self.can_edit = mtool.checkPermission("Modify portal content", context)

        registry = getUtility(IRegistry)
        settings = registry.forInterface(ITypesSchema, prefix="plone")
        link_consent_info_settings = registry.forInterface(
            ILinkConsentInfoControlPanel, prefix="linkconsent"
        )
        self.consent_info_text = link_consent_info_settings.info

        if context.enable_consent_info:
            index = ViewPageTemplateFile("link_consent_info.pt")  # NOQA: F841

        redirect_links = settings.redirect_links

        self.redirect_links = (
            redirect_links
            and not context.enable_consent_info
            and not self._url_uses_scheme(NON_REDIRECTABLE_URL_SCHEMES)
        )

        if self.redirect_links and not self.can_edit:
            target_url = self.absolute_target_url()
            if six.PY2:
                target_url = target_url.encode("utf-8")
            return self.request.RESPONSE.redirect(target_url)
        else:
            return self.index()
