# encoding: utf-8
# Copyright 2011 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

from plone.app.testing import PloneSandboxLayer, IntegrationTesting, FunctionalTesting
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
import jplestd.policy


class JPLESTDSitePolicy(PloneSandboxLayer):
    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)
    def setUpZope(self, app, configurationContext):
        self.loadZCML(package=jplestd.policy)
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'jplestd.policy:default')


JPL_ESTD_POLICY = JPLESTDSitePolicy()
JPL_ESTD_POLICY_INTEGRATION_TESTING = IntegrationTesting(
    bases=(JPL_ESTD_POLICY,),
    name='JPLESTDSitePolicy:Integration'
)
JPL_ESTD_POLICY_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(JPL_ESTD_POLICY,),
    name='JPLESTDSitePolicy:Functional'
)
