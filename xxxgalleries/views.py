from django.views.generic import TemplateView, ListView, View,\
                                 DetailView, CreateView, UpdateView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from models import Gallery, Providers, Tags, Banners
from forms import GalleryForm, ProvidersForm, BannersForm
from django.conf import settings
MEDIA_ROOT = getattr(settings, "MEDIA_ROOT")


class UpdateInstanceView(UpdateView):
    """Todo:
    update providers and banners classes
    to update views to use base UpdateInstanceView
    """
    def form_valid(self, form):
        self.object = form.save(commit=False)
        clean = form.cleaned_data 
        for k, v in clean.items():
            setattr(self.object, k, v)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())



class IndexView(TemplateView):
    """ About Page View """
    template_name = "xxxgalleries/index.html"


class GalleryView(ListView):
    """ Gallery List Page View """
    queryset = Gallery.objects.all().order_by('-id')
    model = Gallery
    paginate_by = 16
    def get_queryset(self, **kwargs):
        return Gallery.objects.filter(content=self.request.GET.get('content', 'pic')).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(GalleryView, self).get_context_data(**kwargs)
        context['tags'] = Tags.objects.all().order_by('name')
        return context


class CreateGallery(CreateView):
    """ Create Gallery page view """
    form_class = GalleryForm
    model = Gallery


class UpdateGallery(UpdateInstanceView):
    """ Update view """
    model = Gallery
    form_class = GalleryForm
    template_name = 'xxxgalleries/gallery_update.html'
    def get_object(self, queryset=None):
        obj = Gallery.objects.get(id=self.kwargs['pk'])
        return obj

    
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
    form_class = ProvidersForm
    template_name = 'xxxgalleries/provider_update.html'

    def get_object(self, queryset=None):
        obj = Providers.objects.get(id=self.kwargs['pk'])
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        clean = form.cleaned_data 
        for k, v in clean.items():
            setattr(self.object, k, v)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProviderDetailView(DetailView):
    """ Gallery Detail Page View """
    queryset = Providers.objects.all()
    def get_object(self, **kwargs):
        """Get the object"""
        object = super(ProviderDetailView, self).get_object(**kwargs)
        return object
    def get_context_data(self, **kwargs):
        context = super(ProviderDetailView, self).get_context_data(**kwargs)
        context['galleries_count'] = Gallery.objects.filter(provider=context.get('object')).count()
        context['banners_count'] = Banners.objects.filter(provider=context.get('object')).count()
        return context



class TagsView(ListView):
    """ Tags List Page View """
    queryset = Tags.objects.all().order_by('name')
    model = Tags


class TagsDetailView(DetailView):
    """ Tags Detail Page View """
    queryset = Tags.objects.all()
    def get_context_data(self, **kwargs):
        context = super(TagsDetailView, self).get_context_data(**kwargs)
        context['galleries'] = Gallery.objects.filter(
                                    tags__pk=context.get('object').pk)
        return context

    def get_object(self, **kwargs):
        object = super(TagsDetailView, self).get_object(**kwargs)
        return object


class AddTagToGallery(View):
    """ Add a tag to a gallery. """
    def get(self, request):
        """Sends back the form to the user and renders the template."""
        raise Http404

    def post(self, request):
        """Process the post request. Boat is required in the post data."""
        gallery = request.POST.get('gallery_id')
        tag = request.POST.get('tag_name')
        tagsplit = tag.split(',')
        for tags in tagsplit:
            if tags[:1] == ' ':
                tags = tags[1:]
            tag_name = str(tags).lower()
            obj, created = Tags.objects.get_or_create(name=tag_name)
            try:
                g = Gallery.objects.get(pk=int(gallery))
            except (ValueError, Gallery.DoesNotExist):
                raise Http404
            g.tags.add(obj)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class RemoveTagFromGallery(View):
    """Add a tag to a gallery """
    def get(self, request):
        """Sends back the form to the user and renders the template."""
        raise Http404

    def post(self, request):
        """Process the post request. Boat is required in the post data."""
        gallery = request.POST.get('gallery_id')
        tag = request.POST.get('tag_name')
        tagsplit = tag.split(',')
        for tags in tagsplit:
            if tags[:1] == ' ':
                tags = tags[1:]
            tag_name = str(tags).lower()
            obj, created = Tags.objects.get_or_create(name=tag_name)
            try:
                g = Gallery.objects.get(pk=int(gallery))
            except (ValueError, Gallery.DoesNotExist):
                raise Http404
            g.tags.remove(obj)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class BannersView(ListView):
    """ Providers List Page View """
    model = Banners


class CreateBanners(CreateView):
    """ Create Gallery page view """
    model = Banners


class UpdateBanners(UpdateView):
    """ Update view """
    model = Banners
    form_class = BannersForm
    template_name = 'xxxgalleries/banners_update\.html'

    def get_object(self, queryset=None):
        obj = Bannerss.objects.get(id=self.kwargs['pk'])
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        clean = form.cleaned_data 
        for k, v in clean.items():
            setattr(self.object, k, v)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class BannersDetailView(DetailView):
    """ Gallery Detail Page View """
    queryset = Banners.objects.all()
    def get_object(self, **kwargs):
        """Get the object"""
        object = super(BannersDetailView, self).get_object(**kwargs)
        return object
