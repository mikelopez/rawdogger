from django.conf.urls import patterns, include, url
from django.conf import settings

from xxxgalleries.views import IndexView, \
        GalleryView, GalleryDetailView, CreateGallery, UpdateGallery, \
        CreateProvider, UpdateProvider, ProviderView, ProviderDetailView, \
        TagsView, TagsDetailView, AddTagToGallery, RemoveTagFromGallery, \
        CreateBanners, UpdateBanners, BannersView, BannersDetailView
        

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

    url(r'^banners/add', CreateBanners.as_view(), name="banners_add"),
    url(r'^banners/update/(?P<pk>\d+)/$', UpdateBanners.as_view(), name="banners_update"),
    url(r'^banners/(?P<pk>\d+)/$', BannersDetailView.as_view(), name="banners_detail"),
    url(r'^banners/', BannersView.as_view(), name="banners_view"),
    
    url(r'^tag/(?P<pk>\d+)/$', TagsDetailView.as_view(), name="tags_detail"),
    url(r'^tags/', TagsView.as_view(), name="tags_view"),
    url(r'^addtag/', AddTagToGallery.as_view(), name="addtag"),
    url(r'^deltag/', RemoveTagFromGallery.as_view(), name="deltag"),
)
