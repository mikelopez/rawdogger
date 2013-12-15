from django import forms 
from django.forms import ModelForm
from models import Gallery, Providers, Banners, ProviderAccounts


class GalleryForm(ModelForm):
    """Gallery Custom form"""
    class Meta:
        model = Gallery
        exclude = ('tags', 'thumb_upload', 
                   'banners', 'filter_name')

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)


class ProvidersForm(ModelForm):
    """Gallery Custom form"""
    class Meta:
        model = Providers

    def __init__(self, *args, **kwargs):
        super(ProvidersForm, self).__init__(*args, **kwargs)
        

class ProviderAccountsForm(ModelForm):
    """Gallery Custom form"""
    class Meta:
        model = ProviderAccounts

    def __init__(self, *args, **kwargs):
        super(ProviderAccountsForm, self).__init__(*args, **kwargs)


class BannersForm(ModelForm):
    """Banners Custom form"""
    class Meta:
        model = Banners

    def __init__(self, *args, **kwargs):
        super(BannersForm, self).__init__(*args, **kwargs)
        
