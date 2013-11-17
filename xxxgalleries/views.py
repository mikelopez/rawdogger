from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render
from models import Gallery, Providers
#from forms import GalleryForm, CategoryForm

class IndexView(TemplateView):
    """ About Page View """
    template_name = "index.html"

class GalleryView(ListView):
    """ Gallery List Page View """
    model = Gallery

class CreateGallery(CreateView):
    """ Create Gallery page view """
    model = Gallery

class UpdateGallery(UpdateView):
    """ Update view """
    model = Gallery
    
class GalleryDetailView(DetailView):
    """ Gallery Detail Page View """
    queryset = Gallery.objects.all()
    def get_object(self, **kwargs):
        object = super(GalleryDetailView, self).get_object(**kwargs)
        return object

class ProviderView(ListView):
    """ Providers List Page View """
    model = Providers

class CreateProvider(CreateView):
    """ Create Gallery page view """
    model = Providers

class UpdateProvider(UpdateView):
    """ Update view """
    model = Providers
    
class ProviderDetailView(DetailView):
    """ Gallery Detail Page View """
    queryset = Providers.objects.all()
    def get_object(self, **kwargs):
        """Get the object"""
        object = super(ProviderDetailView, self).get_object(**kwargs)
        return object

