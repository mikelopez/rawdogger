import simplejson
from django.views.generic import TemplateView, ListView, View,\
                                 DetailView, CreateView, UpdateView
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from models import Gallery, Providers, Tags, Banners, ProviderAccounts, \
                   ProviderWebsites, ProviderWebsiteLinks
from forms import GalleryForm, ProvidersForm, BannersForm, ProviderAccountsForm
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.conf import settings

MEDIA_ROOT = getattr(settings, "MEDIA_ROOT")


class UpdateInstanceView( UpdateView):
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


class SetTagType(StaffuserRequiredMixin, View):
    """
    Set the tag type
    """
    def get(self, request):
        tagid = request.GET.get('tagid', None)
        tagtype = request.GET.get('tagtype', '')
        data = {}
        try:
            tag = Tags.objects.get(pk=int(tagid))
            try:
                setattr(tag, "%s_tag" % (tagtype), True)
                tag.save()
                data['result'] = 'ok'
            except AttributeError:
                data['result'] = 'error'
                data['message'] = 'Not a valid type'
        except (ValueError, Tags.DoesNotExist):
            data['result'] = 'error'
            data['message'] = 'Invalid Tag ID'
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")

    def post(self, request):
        raise Http404


class RemoveTagType(LoginRequiredMixin, StaffuserRequiredMixin, View):
    """
    Set the tag type
    """
    def get(self, request):
        tagid = request.GET.get('tagid', None)
        tagtype = request.GET.get('tagtype', '')
        data = {}
        try:
            tag = Tags.objects.get(pk=int(tagid))
            try:
                setattr(tag, "%s_tag" % (tagtype), False)
                tag.save()
                data['result'] = 'ok'
            except AttributeError:
                data['result'] = 'error'
                data['message'] = 'Not a valid type'
        except (ValueError, Tags.DoesNotExist):
            data['result'] = 'error'
            data['message'] = 'Invalid Tag ID'
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")

    def post(self, request):
        raise Http404



class IndexView(StaffuserRequiredMixin, TemplateView):
    """ About Page View """
    template_name = "xxxgalleries/index.html"


class GalleryView(StaffuserRequiredMixin, ListView):
    """ Gallery List Page View """
    queryset = Gallery.objects.all().order_by('-id')
    model = Gallery
    paginate_by = 16
    def get_queryset(self, **kwargs):
        if self.request.GET.get('content', 'pic') == "pic":
            self.paginate_by = 40
        return Gallery.objects.filter(content=self.request.GET.get('content', 'pic')).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(GalleryView, self).get_context_data(**kwargs)
        context['content'] = self.request.GET.get('content', 'pic')
        context['tags'] = Tags.objects.all().order_by('name')
        return context


class CreateGallery(StaffuserRequiredMixin, CreateView):
    """ Create Gallery page view """
    form_class = GalleryForm
    model = Gallery


class UpdateGallery(StaffuserRequiredMixin, UpdateInstanceView):
    """ Update view """
    model = Gallery
    form_class = GalleryForm
    template_name = 'xxxgalleries/gallery_update.html'
    def get_object(self, queryset=None):
        obj = Gallery.objects.get(id=self.kwargs['pk'])
        return obj

    
class GalleryDetailView(StaffuserRequiredMixin, DetailView):
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
            try:
                for i in obj.show_media():
                    media.append({'filename': i, 'obj': None})
            except:
                pass
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



class ProviderView(StaffuserRequiredMixin, ListView):
    """ Providers List Page View """
    model = Providers

class CreateProvider(StaffuserRequiredMixin, CreateView):
    """ Create Gallery page view """
    model = Providers


class UpdateProvider(StaffuserRequiredMixin, UpdateView):
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


class ProviderDetailView(StaffuserRequiredMixin, DetailView):
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



class TagsView(StaffuserRequiredMixin, ListView):
    """ Tags List Page View """
    queryset = Tags.objects.all().order_by('name')
    model = Tags
    def get_queryset(self, **kwargs):
        filters = {}
        if self.request.GET.get('tagtype', None):
            filters = {'%s_tag'%(self.request.GET.get('tagtype','')): True}
        return Tags.objects.filter(**filters).order_by('name')


class TagsDetailView(StaffuserRequiredMixin, DetailView):
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


class AddTagToGallery(StaffuserRequiredMixin, View):
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


class RemoveTagFromGallery(StaffuserRequiredMixin, View):
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



class BannersView(StaffuserRequiredMixin, ListView):
    """ Providers List Page View """
    model = Banners


class CreateBanners(StaffuserRequiredMixin, CreateView):
    """ Create Gallery page view """
    model = Banners


class UpdateBanners(StaffuserRequiredMixin, UpdateView):
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


class BannersDetailView(StaffuserRequiredMixin, DetailView):
    """ Gallery Detail Page View """
    queryset = Banners.objects.all()
    def get_object(self, **kwargs):
        """Get the object"""
        object = super(BannersDetailView, self).get_object(**kwargs)
        return object


class ProviderAccountsView(StaffuserRequiredMixin, ListView):
    """ Providers List Page View """
    model = ProviderAccounts

class CreateProviderAccounts(StaffuserRequiredMixin, CreateView):
    """ Create Gallery page view """
    model = ProviderAccounts


class UpdateProviderAccounts(StaffuserRequiredMixin, UpdateView):
    """ Update view """
    model = ProviderAccounts
    form_class = ProviderAccountsForm
    template_name = 'xxxgalleries/provider_update.html'

    def get_object(self, queryset=None):
        obj = ProviderAccounts.objects.get(id=self.kwargs['pk'])
        return obj

    def form_valid(self, form):
        self.object = form.save(commit=False)
        clean = form.cleaned_data 
        for k, v in clean.items():
            setattr(self.object, k, v)
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class ProviderAccountsDetailView(StaffuserRequiredMixin, DetailView):
    """ Gallery Detail Page View """
    queryset = ProviderAccounts.objects.all()
    def get_object(self, **kwargs):
        """Get the object"""
        object = super(ProviderAccountsDetailView, self).get_object(**kwargs)
        return object
    def get_context_data(self, **kwargs):
        context = super(ProviderAccountsDetailView, self).get_context_data(**kwargs)
        context['galleries_count'] = Gallery.objects.filter(provider=context.get('object')).count()
        context['banners_count'] = Banners.objects.filter(provider=context.get('object')).count()
        return context
