from baseviews import *




class IndexView(StaffuserRequiredMixin, TemplateView):
    """ About Page View """
    template_name = "xxxgalleries/index.html"


# Gallery
class GalleryView(StaffuserRequiredMixin, ListView):
    """ Gallery List Page View """
    queryset = Gallery.objects.all().order_by('-id')
    model = Gallery
    paginate_by = 16
    def get_queryset(self, **kwargs):
        if self.request.GET.get('content', 'pic') == "pic":
            self.paginate_by = 21
        return Gallery.objects.filter(content=self.request.GET.get('content', 'pic')).order_by('-id')

    def get_context_data(self, **kwargs):
        context = super(GalleryView, self).get_context_data(**kwargs)
        context['content'] = self.request.GET.get('content', 'pic')
        context['tags'] = Tags.objects.all().order_by('name')
        try:
            context['tag_selected'] = Tags.objects.get(pk=self.request.GET.get('tag', None))
        except (Tags.DoesNotExist, ValueError):
            context['tag_selected'] = None
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



# Providers
class ProviderView(StaffuserRequiredMixin, ListView):
    """ Providers List Page View """
    model = Providers

class CreateProvider(StaffuserRequiredMixin, CreateView):
    """ Create Provider page view """
    model = Providers

class UpdateProvider(StaffuserRequiredMixin, UpdateInstanceView):
    """ Update view """
    model = Providers
    form_class = ProvidersForm
    template_name = 'xxxgalleries/provider_update.html'
    def get_object(self, queryset=None):
        obj = Providers.objects.get(id=self.kwargs['pk'])
        return obj

class ProviderDetailView(StaffuserRequiredMixin, DetailView):
    """ Provider detail Page View """
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



# ProviderAccounts
class ProviderAccountsView(StaffuserRequiredMixin, ListView):
    """ Provider Accounts List Page View """
    model = ProviderAccounts

class CreateProviderAccounts(StaffuserRequiredMixin, CreateView):
    """ Create Provider account page view """
    model = ProviderAccounts

class UpdateProviderAccounts(StaffuserRequiredMixin, UpdateInstanceView):
    """ Update view """
    model = ProviderAccounts
    form_class = ProviderAccountsForm
    template_name = 'xxxgalleries/provideraccounts_update.html'
    def get_object(self, queryset=None):
        obj = ProviderAccounts.objects.get(id=self.kwargs['pk'])
        return obj

class ProviderAccountsDetailView(StaffuserRequiredMixin, DetailView):
    """ Provider Accounts Page View """
    queryset = ProviderAccounts.objects.all()
    def get_object(self, **kwargs):
        """Get the object"""
        object = super(ProviderAccountsDetailView, self).get_object(**kwargs)
        return object
    def get_context_data(self, **kwargs):
        context = super(ProviderAccountsDetailView, self).get_context_data(**kwargs)
        context['program_types'] = ProgramTypes.objects.filter(account=context.get('object'))
        #context['banners_count'] = Banners.objects.filter(provider=context.get('object')).count()
        return context



# ProgramTypes
class ProgramTypesView(StaffuserRequiredMixin, ListView):
    """ Program Types List Page View """
    model = ProgramTypes

class CreateProgramTypes(StaffuserRequiredMixin, CreateView):
    """ Create ProgramTypes page view """
    model = ProgramTypes

class UpdateProgramTypes(StaffuserRequiredMixin, UpdateInstanceView):
    """ Update view """
    model = ProgramTypes
    form_class = ProgramTypesForm
    template_name = 'xxxgalleries/programtypes_update.html'
    def get_object(self, queryset=None):
        obj = ProgramTypes.objects.get(id=self.kwargs['pk'])
        return obj

class ProgramTypesDetailView(StaffuserRequiredMixin, DetailView):
    """ Program Types Page View """
    queryset = ProgramTypes.objects.all()
    def get_object(self, **kwargs):
        """Get the object"""
        object = super(ProgramTypesDetailView, self).get_object(**kwargs)
        return object
    def get_context_data(self, **kwargs):
        context = super(ProgramTypesDetailView, self).get_context_data(**kwargs)
        context['account_id'] = self.request.GET.get('account_id', None)
        #context['galleries_count'] = Gallery.objects.filter(provider=context.get('object')).count()
        #context['banners_count'] = Banners.objects.filter(provider=context.get('object')).count()
        return context


# ProviderWebsites
class ProviderWebsitesView(StaffuserRequiredMixin, ListView):
    """ Program Types List Page View """
    model = ProviderWebsites

class CreateProviderWebsites(StaffuserRequiredMixin, CreateView):
    """ Create ProgramTypes page view """
    model = ProviderWebsites

class UpdateProviderWebsites(StaffuserRequiredMixin, UpdateInstanceView):
    """ Update view """
    model = ProviderWebsites
    form_class = ProviderWebsitesForm
    template_name = 'xxxgalleries/providerwebsites_update.html'
    def get_object(self, queryset=None):
        obj = ProviderWebsites.objects.get(id=self.kwargs['pk'])
        return obj

class ProviderWebsitesDetailView(StaffuserRequiredMixin, DetailView):
    """ Program Types Page View """
    queryset = ProviderWebsites.objects.all()
    def get_object(self, **kwargs):
        """Get the object"""
        object = super(ProviderWebsitesDetailView, self).get_object(**kwargs)
        return object
    def get_context_data(self, **kwargs):
        context = super(ProviderWebsitesDetailView, self).get_context_data(**kwargs)
        #context['galleries_count'] = Gallery.objects.filter(provider=context.get('object')).count()
        #context['banners_count'] = Banners.objects.filter(provider=context.get('object')).count()
        return context


# ProviderWebsiteLinks
class ProviderWebsiteLinksView(StaffuserRequiredMixin, ListView):
    """ Program Types List Page View """
    model = ProviderWebsiteLinks

class CreateWebsiteLinks(StaffuserRequiredMixin, CreateView):
    """ Create ProgramTypes page view """
    model = ProviderWebsiteLinks

class UpdateProviderWebsiteLinks(StaffuserRequiredMixin, UpdateInstanceView):
    """ Update view """
    model = ProviderWebsiteLinks
    form_class = ProviderWebsiteLinksForm
    template_name = 'xxxgalleries/providerwebsitelinks_update.html'
    def get_object(self, queryset=None):
        obj = ProviderWebsiteLinks.objects.get(id=self.kwargs['pk'])
        return obj

class ProviderWebsiteLinksDetailView(StaffuserRequiredMixin, DetailView):
    """ Program Types Page View """
    queryset = ProviderWebsiteLinks.objects.all()
    def get_object(self, **kwargs):
        """Get the object"""
        object = super(ProviderWebsiteLinksDetailView, self).get_object(**kwargs)
        return object
    def get_context_data(self, **kwargs):
        context = super(ProviderWebsiteLinksDetailView, self).get_context_data(**kwargs)
        #context['galleries_count'] = Gallery.objects.filter(provider=context.get('object')).count()
        #context['banners_count'] = Banners.objects.filter(provider=context.get('object')).count()
        return context



# Tags
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




# Banners
class BannersView(StaffuserRequiredMixin, ListView):
    """ Banners List Page View """
    model = Banners

class CreateBanners(StaffuserRequiredMixin, CreateView):
    """ Create Banners page view """
    model = Banners

class UpdateBanners(StaffuserRequiredMixin, UpdateInstanceView):
    """ Update view """
    model = Banners
    form_class = BannersForm
    template_name = 'xxxgalleries/banners_update.html'
    def get_object(self, queryset=None):
        obj = Banners.objects.get(id=self.kwargs['pk'])
        return obj

class BannersDetailView(StaffuserRequiredMixin, DetailView):
    """ Banner Detail Page View """
    queryset = Banners.objects.all()
    def get_object(self, **kwargs):
        object = super(BannersDetailView, self).get_object(**kwargs)
        return object




class AddTagToGallery(StaffuserRequiredMixin, AddGalleryTagBase):
    """ Add a tag to a gallery. """
            
    def get(self, request):
        """Sends back the form to the user and renders the template."""
        gallery = request.GET.get('gallery_id')
        tag = request.GET.get('tag_name')
        return self.tagthatbitch(request, gallery, tag, return_type='json', action='add')

    def post(self, request):
        """Process the post request. Boat is required in the post data."""
        gallery = request.POST.get('gallery_id')
        tag = request.POST.get('tag_name')
        return self.tagthatbitch(request, gallery, tag, action='add')


class RemoveTagFromGallery(StaffuserRequiredMixin, AddGalleryTagBase):
    """Add a tag to a gallery """
    def get(self, request):
        """Sends back the form to the user and renders the template."""
        gallery = request.GET.get('gallery_id')
        tag = request.GET.get('tag_name')
        return self.tagthatbitch(request, gallery, tag, return_type='json', action='remove')

    def post(self, request):
        """Process the post request. Boat is required in the post data."""
        gallery = request.POST.get('gallery_id')
        tag = request.POST.get('tag_name')
        return self.tagthatbitch(request, gallery, tag, action='remove')


# Tags configurations
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
