from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render
from models import Gallery
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

