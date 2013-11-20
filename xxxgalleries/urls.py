from django.conf.urls import patterns, include, url
from django.conf import settings

from xxxgalleries.views import IndexView, GalleryView, GalleryDetailView, \
        CreateGallery, UpdateGallery, CreateProvider, UpdateProvider, \
        ProviderView, ProviderDetailView

urlpatterns = patterns('',
    url(r'^$', GalleryView.as_view(), name="xxx_index"),
    url(r'^gallery/add', CreateGallery.as_view(), name="galleries_add"),
    url(r'^gallery/update/(?P<pk>\d+)/$', UpdateGallery.as_view(), name="galleries_update"),
    url(r'^gallery/', GalleryView.as_view(), name="galleries_view"),
    url(r'^galleries/(?P<pk>\d+)/$', GalleryDetailView.as_view(), name="gallery_detail"),

    url(r'^provider/add', CreateProvider.as_view(), name="providers_add"),
    url(r'^provider/update/(?P<pk>\d+)/$', UpdateProvider.as_view(), name="providers_update"),
    url(r'^provider/', ProviderView.as_view(), name="providers_view"),
    url(r'^providers/(?P<pk>\d+)/$', ProviderDetailView.as_view(), name="provider_detail"),
    
)
