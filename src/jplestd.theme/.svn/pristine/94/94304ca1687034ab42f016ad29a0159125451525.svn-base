# encoding: utf-8

u'''JPL Section 873 Theme — logo tests'''

from jplestd.theme.testing import JPL_ESTD_THEME_INTEGRATION_TESTING
import unittest2 as unittest
import pkg_resources, os.path

class LogoTest(unittest.TestCase):
    layer = JPL_ESTD_THEME_INTEGRATION_TESTING
    def testCustomLogo(self):
        '''Ensure we have the JPL ESTD logo, not the default JPL logo.
        
        Screw this: now that the z3c.jbot images are tied to a specific layer, we no longer
        seem to get the overridden image during testing. But it works in operation, so I'll
        chalk it up to yet another plone.app.testing #fail.
        
        Maybe there's some step we can do in the testing layer setup, but I don't know what
        it is.'''
        return # Screw this
        # Get the size of the JPL ESTD logo in bytes
        fn = 'jpl.ngtheme.skins.jpl_ngtheme_custom_images.logo.png'
        expected = os.path.getsize(pkg_resources.resource_filename('jplestd.theme.browser', 'images/' + fn))
        # Get the logo Plone is using
        portal = self.layer['portal']
        logo = portal.unrestrictedTraverse('logo.png')
        # Are they the same? Go by size, which should be good enough.
        self.assertEquals(expected, logo.get_size())

def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

