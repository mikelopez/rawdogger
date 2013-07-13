"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from django.test import TestCase
from settings import PROJECT_ROOTDIR
from xxxgalleries.models import *
from django.contrib.auth.models import *
from decimal import Decimal

class TestModelBase(TestCase):
    """
    Test the web/models schema  
    Create the groups and Users 
    """
    # groups should exist 
    # Captain, Owner, Renter
    table_columns = {
        'Providers': [
            '',
        ],
        'Galleries': [
            '',
        ],
        'ProgramTypes': [
            ''
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
        

