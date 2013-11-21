from django import forms 
from django.forms import ModelForm
from models import Gallery, Providers, Banners


class GalleryForm(ModelForm):
    """Gallery Custom form"""
    class Meta:
        model = Gallery
        exclude = ('tags','thumb_url', 'thumb_upload', 'banners',)

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)


class ProvidersForm(ModelForm):
    """Gallery Custom form"""
    class Meta:
        model = Providers

    def __init__(self, *args, **kwargs):
        super(ProvidersForm, self).__init__(*args, **kwargs)
        

class BannersForm(ModelForm):
    """Banners Custom form"""
    class Meta:
        model = Banners

    def __init__(self, *args, **kwargs):
        super(BannersForm, self).__init__(*args, **kwargs)
        