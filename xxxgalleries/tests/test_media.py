"""
Test the media directories exist holding the media for galleries
"""

import os
from django.test import TestCase
from xxxgalleries.models import *
from django.contrib.auth.models import *
from decimal import Decimal
from django.conf import settings
from termprint import *

PROJECT_ROOTDIR = getattr(settings, "PROJECT_ROOTDIR")
MEDIA_ROOT = getattr(settings, "MEDIA_ROOT")

class TestMediaDirectories(TestCase):
    """
    Test and make sure the media directories exist
    """
    def setUp(self):
        """ Check for project root directory """
        termprint("INFO", 'Checking media directories')
        termprint("WARNING", "\tMEDIA_ROOT = %s" % MEDIA_ROOT)
        #termprint("WARNING", "\tMEDIA_ROOT = %s" % MEDIA_ROOT)
        if not MEDIA_ROOT:
            termprint("ERROR", "Please create the directory: %s" % MEDIA_ROOT)
            assert False, "Media root was not found!"

    def test_base_media(self):
        """Finds teh base media path."""
        self.assertTrue(os.path.exists(MEDIA_ROOT))

    def test_galleries_media(self):
        """Finds the galleries subdirectory in media_root"""
        self.assertTrue(os.path.exists("%s/galleries" % (MEDIA_ROOT)))

    
        

