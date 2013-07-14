"""
Test the media directories exist holding the media for galleries
"""

import os
from django.test import TestCase
from xxxgalleries.models import *
from django.contrib.auth.models import *
from decimal import Decimal
from django.conf import settings
PROJECT_ROOTDIR = getattr(settings, "PROJECT_ROOTDIR", None)

class TestMediaDirectories(TestCase):
    """
    Test and make sure the media directories exist
    """
    def setUp(self):
        """ Check for project root directory """
        print 'Checking media directories\n'
        if not PROJECT_ROOTDIR:
            assert False, "Project Root Directiry is set in settings"

    def test_base_media(self):
        self.assertTrue(os.path.exists(PROJECT_ROOTDIR))

    def test_galleries_media(self):
        self.assertTrue(os.path.exists("%s/xxxgalleries" % (PROJECT_ROOTDIR)))

    
        

