# -*- coding: utf-8 -*-

from Products.Five.browser import BrowserView
from zope.interface import implementer
from zope.interface import Interface
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName
from Products.CMFEditions.utilities import dereference
from plone.protect.interfaces import IDisableCSRFProtection
from zope.interface import alsoProvides


class ICleanRevisions(Interface):
    """Marker Interface for ICleanRevisions"""


@implementer(ICleanRevisions)
class CleanRevisions(BrowserView):
    def __call__(self):
        alsoProvides(self.request, IDisableCSRFProtection)
        policy = getToolByName(self.context, 'portal_purgepolicy')
        catalog = getToolByName(self.context, 'portal_catalog')

        for count, brain in enumerate(catalog()):
            obj = brain.getObject()

            # only purge old content
            if obj.created() < (DateTime()):
                obj, history_id = dereference(obj)
                policy.beforeSaveHook(history_id, obj)
                print('purged revisions of object ' + obj.absolute_url_path())
        return "cleaning finished!"
