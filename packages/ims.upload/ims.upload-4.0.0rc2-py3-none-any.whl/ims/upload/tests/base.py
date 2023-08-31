import os
import unittest

import transaction
from plone.app.testing import setRoles, TEST_USER_ID, SITE_OWNER_NAME, SITE_OWNER_PASSWORD
from plone.testing.zope import Browser
from zope.interface.declarations import directlyProvides

from .. import testing
from ..interfaces import IUploadLayer


class UnitTestCase(unittest.TestCase):
    def setUp(self):
        pass


class IntegrationTestCase(unittest.TestCase):
    layer = testing.INTEGRATION

    def setUp(self):
        super().setUp()
        self.portal = self.layer['portal']
        self.request = self.layer
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.base_path = os.path.dirname(os.path.realpath(__file__))
        directlyProvides(self.portal.REQUEST, IUploadLayer)
        directlyProvides(self.request, IUploadLayer)


class FunctionalTestCase(IntegrationTestCase):
    layer = testing.FUNCTIONAL

    def setUp(self):
        super().setUp()
        self.browser = Browser(self.layer['app'])
        self.browser.handleErrors = False
        self.browser.addHeader(
            'Authorization',
            'Basic %s:%s' % (SITE_OWNER_NAME, SITE_OWNER_PASSWORD,)
        )
        transaction.commit()
