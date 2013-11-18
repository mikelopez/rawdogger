from django import forms, ModelForm
from models import Gallery

class GalleryForm(ModelForm):
	"""Gallery Custom form"""
	class Meta:
		model = Gallery