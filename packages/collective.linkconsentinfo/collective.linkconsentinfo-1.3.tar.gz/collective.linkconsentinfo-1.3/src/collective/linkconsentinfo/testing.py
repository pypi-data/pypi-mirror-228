# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import collective.linkconsentinfo


class CollectiveLinkconsentinfoLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=collective.linkconsentinfo)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.linkconsentinfo:default')


COLLECTIVE_LINKCONSENTINFO_FIXTURE = CollectiveLinkconsentinfoLayer()


COLLECTIVE_LINKCONSENTINFO_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_LINKCONSENTINFO_FIXTURE,),
    name='CollectiveLinkconsentinfoLayer:IntegrationTesting',
)


COLLECTIVE_LINKCONSENTINFO_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_LINKCONSENTINFO_FIXTURE,),
    name='CollectiveLinkconsentinfoLayer:FunctionalTesting',
)


COLLECTIVE_LINKCONSENTINFO_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_LINKCONSENTINFO_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CollectiveLinkconsentinfoLayer:AcceptanceTesting',
)
