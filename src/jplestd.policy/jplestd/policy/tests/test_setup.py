# encoding: utf-8

u'''JPL Data System Technology Office 873 — Site Policy — Tests of the setup of the policy.
'''

from jplestd.policy.testing import JPL_ESTD_POLICY_INTEGRATION_TESTING
from Products.CMFCore.utils import getToolByName
import unittest


class SetupTest(unittest.TestCase):
    '''Unit tests the setup of the site policy.'''
    layer = JPL_ESTD_POLICY_INTEGRATION_TESTING
    def setUp(self):
        super(SetupTest, self).setUp()
        self.portal = self.layer['portal']
    def testPortalTitle(self):
        '''Test if the site's title is set correctly.'''
        self.assertEquals('Data System and Technology Office 873', self.portal.getProperty('title'))
    def testPortalDescription(self):
        '''Test if the site's description is set correctly.'''
        self.assertEquals('Home and intranet for section 873, the Data System and Technology Office.',
            self.portal.getProperty('description'))
    def testMailSettings(self):
        self.assertEquals('Section 873 Site Admin', self.portal.getProperty('email_from_name'))
        self.assertEquals('emily.law@jpl.nasa.gov', self.portal.getProperty('email_from_address'))
    def testIfThemeInstalled(self):
        skins = getToolByName(self.portal, 'portal_skins')
        self.assertEquals('JPL Section 873 Theme', skins.getDefaultSkin())
    def testGlobalNavProperties(self):
        props = getToolByName(self.portal, 'portal_properties')
        self.failUnless(props.site_properties.getProperty('disable_nonfolderish_sections'))
        self.failUnless(props.navtree_properties.getProperty('enable_wf_state_filtering'))
        self.failUnless(u'published' in props.navtree_properties.getProperty('wf_states_to_show'))
    def testCarousel(self):
        u'''Ensure the carousel is installed'''
        qi = getToolByName(self.portal, 'portal_quickinstaller')
        self.assertTrue(qi.isProductInstalled('Carousel'), u'Carousel not installed')
        
def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')