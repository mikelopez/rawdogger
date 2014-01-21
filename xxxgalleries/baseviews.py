import simplejson
from django.views.generic import TemplateView, ListView, View,\
                                 DetailView, CreateView, UpdateView
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from models import Gallery, Providers, Tags, Banners, ProviderAccounts, \
                   ProviderWebsites, ProviderWebsiteLinks, ProgramTypes
from forms import GalleryForm, ProvidersForm, BannersForm, ProviderAccountsForm, \
                   ProgramTypesForm, ProviderWebsitesForm, ProviderWebsiteLinksForm
from braces.views import LoginRequiredMixin, StaffuserRequiredMixin
from django.conf import settings

MEDIA_ROOT = getattr(settings, "MEDIA_ROOT")


class AddGalleryTagBase(View):
    """Base View Class containing gallery-tag adding functionality"""
    def tagthatbitch(self, request, gallery, tag, return_type="html", action=""):
        tagsplit = tag.split(',')
        data = {'result': 'ok', 'message': 'ok'}
        for tags in tagsplit:
            if tags[:1] == ' ':
                tags = tags[1:]
            tag_name = str(tags).lower()
            obj, created = Tags.objects.get_or_create(name=tag_name)
            try:
                g = Gallery.objects.get(pk=int(gallery))
            except (ValueError, Gallery.DoesNotExist):
                if return_type == 'html':
                    raise Http404
                else:
                    data['result'] = 'error'
                    data['message'] = 'No gallery found with id %s' % gallery
            if action == 'add':
                g.tags.add(obj)
            if action == 'remove': 
                g.tags.remove(obj)
        if return_type == "json":
            return HttpResponse(simplejson.dumps(data), mimetype="application/json")
        if return_type == "html":
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

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

