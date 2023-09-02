# -*- coding: utf-8 -*-
from collective.linkconsentinfo import _
from plone import schema
from plone.app.registry.browser.controlpanel import (
    ControlPanelFormWrapper,
    RegistryEditForm,
)
# from plone.autoform import directives
from plone.z3cform import layout
from zope.interface import Interface


class ILinkConsentInfoControlPanel(Interface):
    """ LinkConsentInfoControlPanel schema
    """

    # directives.widget("info", klass="pat-tinymce")
    info = schema.Text(
        title=_(u"Consent Info Message",),
        description=_(u"The info messaged shown to users, when they click on a link. \nYou can use HTML-Syntax here.",),
        required=False,
        default=_(u"""<h1>You are about to leave this Website</h1>
<p>You are about to open an external website, we are not accountable for the content of external websites.</p>
<p>Please note the data privacy rules of that website!</p>"""),
    )


class LinkConsentInfoControlPanelForm(RegistryEditForm):
    schema = ILinkConsentInfoControlPanel
    schema_prefix = "linkconsent"
    label = u"Link Consent Settings"


LinkConsentInfoControlPanelView = layout.wrap_form(
    LinkConsentInfoControlPanelForm, ControlPanelFormWrapper
)
