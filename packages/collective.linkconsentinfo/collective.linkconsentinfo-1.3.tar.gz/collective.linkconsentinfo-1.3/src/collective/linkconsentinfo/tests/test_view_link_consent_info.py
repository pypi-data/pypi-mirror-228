# -*- coding: utf-8 -*-
from collective.linkconsentinfo.testing import (
    COLLECTIVE_LINKCONSENTINFO_FUNCTIONAL_TESTING,
    COLLECTIVE_LINKCONSENTINFO_INTEGRATION_TESTING,
)
from plone import api
from plone.app.testing import setRoles, TEST_USER_ID
from zope.component import getMultiAdapter
from zope.component.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_LINKCONSENTINFO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, 'Link', 'external-link')
        api.content.create(self.portal, 'Document', 'front-page')

    def test_link_consent_info_is_registered(self):
        view = getMultiAdapter(
            (self.portal['external-link'], self.portal.REQUEST),
            name='link_redirect_view'
        )
        self.assertTrue(view.__name__ == 'link_redirect_view')
        self.assertTrue(view.index.filename.endswith("link_consent_info.pt"))

    def test_link_consent_info_not_matching_interface(self):
        with self.assertRaises(ComponentLookupError):
            getMultiAdapter(
                (self.portal['front-page'], self.portal.REQUEST),
                name='link_redirect_view'
            )


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_LINKCONSENTINFO_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
