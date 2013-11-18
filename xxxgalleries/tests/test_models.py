"""
Tests the models and forms. 
"""

from django.test import TestCase
from django.conf import settings
from xxxgalleries.models import *
from django.contrib.auth.models import *
from decimal import Decimal

PROJECT_ROOTDIR = getattr(settings, "PROJECT_ROOTDIR", None)

class TestBaseModels(TestCase):
    """
    Test the web/models schema  
    Create the groups and Users 
    """
    # groups should exist 
    # Captain, Owner, Renter
    table_columns = {
        'Providers': [
            'name',
            'username',
            'password',
            'website',
            'login_url',
            'ccbill',
            'notes'
        ],
        'Gallery': [
            'name',
            'gallery_type',
            'provider'
        ],
        'ProgramTypes': [
            'name',
            'provider',
            'notes'
        ]
    }
        

    def test_tablecolumns(self):
        print "Running Model Tests.....\n"
        for k,v in self.table_columns.items():
            for l in v:
                print 'Checking Table %s for column %s...' % (k, l)
                try:
                    d = eval(k)()
                    dattr = getattr(d, l)
                except AttributeError:
                    assert False, "Error %s / %s" % (k, v)
                except:
                    pass
        

