from django import forms 
from django.forms import ModelForm
from models import Gallery, Providers

class GalleryForm(ModelForm):
    """Gallery Custom form"""
    class Meta:
        model = Gallery
        exclude = ('tags','thumb_url', 'thumb_upload',)

    def __init__(self, *args, **kwargs):
        super(GalleryForm, self).__init__(*args, **kwargs)
        #self.fields['thumb_url'].widget = forms.TextInput()
        #self.fields['hosted_jump_link'].widget = forms.TextInput()


class ProvidersForm(ModelForm):
    """Gallery Custom form"""
    class Meta:
        model = Providers

    def __init__(self, *args, **kwargs):
        super(ProvidersForm, self).__init__(*args, **kwargs)
        
