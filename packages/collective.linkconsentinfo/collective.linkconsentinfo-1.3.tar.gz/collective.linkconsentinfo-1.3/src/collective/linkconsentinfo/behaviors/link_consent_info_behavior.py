# -*- coding: utf-8 -*-

from collective.linkconsentinfo import _
from plone import schema
from plone.app.z3cform.widget import SingleCheckBoxBoolFieldWidget
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from Products.CMFPlone.utils import safe_hasattr
from zope.component import adapter
from zope.interface import implementer, Interface, provider


class ILinkConsentInfoBehaviorMarker(Interface):
    pass


@provider(IFormFieldProvider)
class ILinkConsentInfoBehavior(model.Schema):
    """ LinkConsentInfoBehavior schema interface
    """

    directives.widget(enable_consent_info=SingleCheckBoxBoolFieldWidget)
    enable_consent_info = schema.Bool(
        title=_(u"Enable Consent Info",),
        description=_(u"This will enable a consent info page for this link.",),
        default=False,
    )


@implementer(ILinkConsentInfoBehavior)
@adapter(ILinkConsentInfoBehaviorMarker)
class LinkConsentInfoBehavior(object):
    def __init__(self, context):
        self.context = context

    @property
    def enable_consent_info(self):
        if safe_hasattr(self.context, "enable_consent_info"):
            return self.context.enable_consent_info
        return None

    @enable_consent_info.setter
    def enable_consent_info(self, value):
        self.context.enable_consent_info = value
