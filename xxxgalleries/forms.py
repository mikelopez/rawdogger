from django import forms 
from django.forms import ModelForm
from models import Gallery, Providers, Banners, ProviderAccounts, ProgramTypes, \
                    ProviderWebsites, ProviderWebsiteLinks


class BaseForm(ModelForm):
    """Providers Custom form"""
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)

class GalleryForm(ModelForm):
    """Gallery Custom form"""
    class Meta:
        model = Gallery
        exclude = ('tags', 'thumb_upload', 
                   'banners', 'filter_name')

class ProvidersForm(BaseForm):
    """Providers Custom form"""
    class Meta:
        model = Providers

class ProviderWebsitesForm(BaseForm):
    """Program types Custom form"""
    class Meta:
        model = ProviderWebsites

class ProviderWebsiteLinksForm(BaseForm):
    """Program types Custom form"""
    class Meta:
        model = ProviderWebsiteLinks

class ProgramTypesForm(BaseForm):
    """Program types Custom form"""
    class Meta:
        model = ProgramTypes 
        exclude = ('provider',) 

class ProviderAccountsForm(BaseForm):
    """Provider accoutns Custom form"""
    class Meta:
        model = ProviderAccounts

class BannersForm(BaseForm):
    """Banners Custom form"""
    class Meta:
        model = Banners

        
