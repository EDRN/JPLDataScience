# encoding: utf-8

from plone.app.testing import PloneSandboxLayer, IntegrationTesting, FunctionalTesting
from jpl.ngtheme.testing import JPL_NEXT_GENERATION_THEME
from plone.testing import z2

class JPLESTDTheme(PloneSandboxLayer):
    defaultBases = (JPL_NEXT_GENERATION_THEME,)
    def setUpZope(self, app, configurationContext):
        import jplestd.theme
        self.loadZCML(package=jplestd.theme)
        z2.installProduct(app, 'jplestd.theme')
    def setUpPloneSite(self, portal):
        self.applyProfile(portal, 'jplestd.theme:default')
    def tearDownZope(self, app):
        z2.uninstallProduct(app, 'jplestd.theme')
    
JPL_ESTD_THEME = JPLESTDTheme()
JPL_ESTD_THEME_INTEGRATION_TESTING = IntegrationTesting(
    bases=(JPL_ESTD_THEME,),
    name='JPLESTDTheme:Integration'
)
JPL_ESTD_THEME_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(JPL_ESTD_THEME,),
    name='JPLESTDTheme:Functional'
)
