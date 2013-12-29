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
MY_TEST_SITE = "mytestsite.com"

class TestProviders(TestCase):
    """
    Test and make sure the media directories exist
    """
    provider_attrs = {
        'name': 'ProviderTest',
        'website': 'http://www.provider.com',
        'login_url': 'http://www.provider.com/login',
    }

    def __create_provider_sites(self):
        """
        Creates 3 provider sites.
        These are the websites that an affiliate network offers promotion for.
        """
        for i in range(0, 2):
            domain = "providersite%s.com" % i
            psite = ProviderWebsites(**{'provider': self.provider, 'website': domain})
            psite.save()

    def setUp(self):
        """ Check for project root directory """
        self.provider = Provider(**self.provider_attrs)
        self.provider.save()

        # create some sites for the provider
        self.__create_provider_sites()


    def test_provider_links(self):
        """Test creating and getting provider links
        by replacing placeholder text with affiliate ID information
        for the particular site/link/program type combo."""

        # 1) Create the account
        account_attrs = {'provider': self.provider,
                         'email_registered': 'test@emails.com',
                         'username': 'user1', 'password': 'pass123',
                         'website_registered': MY_TEST_SITE,
                         'ccbill': '111111', 'affiliate_id': '222222',
                         'link_id': 'sciweb'
        }
        account = ProviderAccounts(**account_attrs)

        revshare = ProgramTypes(**{'account': account, 'name': 'Revshare',
                                       'link_id': 'sciweb.revshare.twistys'})
        
        pps = ProgramTypes(**{'account': account, 'name': 'PPS 35$',
                                       'link_id': 'sciweb.pps.twistys'})
        revshare.save()
        pps.save()

        websites = ProviderWebsites.objects.all()
        provider_websites = ProviderWebsiteLinks(**{'website': websites[0], 
                                                    'program_type': pps,
                                                    'name': 'Nasty bitches1',
                                                    'url': 'http://www.nastybitches.com/?id=#AFFILIATE_ID#'})
        provider_websites.save()


        # test some logic here todo

    
        

