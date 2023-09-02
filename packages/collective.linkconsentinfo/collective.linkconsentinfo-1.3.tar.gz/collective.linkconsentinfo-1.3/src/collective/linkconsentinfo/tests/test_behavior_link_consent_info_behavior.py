# -*- coding: utf-8 -*-
from collective.linkconsentinfo.behaviors.link_consent_info_behavior import (
    ILinkConsentInfoBehaviorMarker,
)
from collective.linkconsentinfo.testing import (  # noqa,,,,
    COLLECTIVE_LINKCONSENTINFO_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles, TEST_USER_ID
from plone.behavior.interfaces import IBehavior
from zope.component import getUtility

import unittest


class LinkConsentInfoBehaviorIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_LINKCONSENTINFO_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_behavior_link_consent_info_behavior(self):
        behavior = getUtility(
            IBehavior, "collective.linkconsentinfo.link_consent_info_behavior"
        )
        self.assertEqual(
            behavior.marker, ILinkConsentInfoBehaviorMarker,
        )
