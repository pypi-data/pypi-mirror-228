# -*- coding: utf-8 -*-
from collective.linkconsentinfo.testing import (
    COLLECTIVE_LINKCONSENTINFO_FUNCTIONAL_TESTING,
    COLLECTIVE_LINKCONSENTINFO_INTEGRATION_TESTING,
)
from plone.app.testing import setRoles, TEST_USER_ID

import unittest


class IndexerIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_LINKCONSENTINFO_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_dummy(self):
        self.assertTrue(True)


class IndexerFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_LINKCONSENTINFO_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_dummy(self):
        self.assertTrue(True)
