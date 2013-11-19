from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from django.shortcuts import render
from models import Gallery, Providers
from forms import GalleryForm
from django.conf import settings
MEDIA_ROOT = getattr(settings, "MEDIA_ROOT")

class IndexView(TemplateView):
    """ About Page View """
    template_name = "index.html"

class GalleryView(ListView):
    """ Gallery List Page View """
    model = Gallery

class CreateGallery(CreateView):
    """ Create Gallery page view """
    model_class = GalleryForm
    model = Gallery

class UpdateGallery(UpdateView):
    """ Update view """
    model = Gallery
    context_object_name = 'object'
    
class GalleryDetailView(DetailView):
    """ Gallery Detail Page View """
    queryset = Gallery.objects.all()
    def get_context_data(self, **kwargs):
        context = super(GalleryDetailView, self).get_context_data(**kwargs)
        context['MEDIA_ROOT'] = MEDIA_ROOT
        obj = context.get('object')
        # add the media either from DB (if any) or from local FS
        media = []
        if obj.is_sync:
            for i in obj.galleryitem_set.select_related():
                media.append({'filename': i.filename, 'obj': i})
        else:
            for i in obj.show_media():
                media.append({'filename': i, 'obj': None})
        thumb = None
        for m in media:
            if 'thumb' in m.get('filename'):
                thumb = m
        context['thumbnail'] = thumb
        context['media'] = media
        return context

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

