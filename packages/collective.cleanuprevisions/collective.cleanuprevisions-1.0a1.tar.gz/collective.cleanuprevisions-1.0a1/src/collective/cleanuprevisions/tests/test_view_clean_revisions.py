# -*- coding: utf-8 -*-
from collective.cleanuprevisions.testing import (
    COLLECTIVE_CLEANUPREVISIONS_FUNCTIONAL_TESTING,
)
from collective.cleanuprevisions.testing import (
    COLLECTIVE_CLEANUPREVISIONS_INTEGRATION_TESTING,
)
from collective.cleanuprevisions.views.clean_revisions import ICleanRevisions
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from zope.component import getMultiAdapter
from zope.interface.interfaces import ComponentLookupError

import unittest


class ViewsIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_CLEANUPREVISIONS_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
        api.content.create(self.portal, "Folder", "other-folder")
        api.content.create(self.portal, "Document", "front-page")

    def test_clean_revisions_is_registered(self):
        view = getMultiAdapter(
            (self.portal["other-folder"], self.portal.REQUEST), name="clean-revisions"
        )
        self.assertTrue(ICleanRevisions.providedBy(view))

    def test_clean_revisions_not_matching_interface(self):
        view_found = True
        try:
            view = getMultiAdapter(
                (self.portal["front-page"], self.portal.REQUEST), name="clean-revisions"
            )
        except ComponentLookupError:
            view_found = False
        else:
            view_found = ICleanRevisions.providedBy(view)
        self.assertFalse(view_found)


class ViewsFunctionalTest(unittest.TestCase):

    layer = COLLECTIVE_CLEANUPREVISIONS_FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])
