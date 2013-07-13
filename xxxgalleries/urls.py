from django.conf.urls import patterns, include, url
from django.conf import settings


urlpatterns = patterns('',
    #url(r'^$', 'xxxgalleries.xxxgalleries.views.main_index', name='main_index'),
    url(r'^gallery/add', CreateGallery.as_view(), name="galleries-add"),
    url(r'^gallery/update', UpdateGallery.as_view(), name="galleries-update"),
    url(r'^gallery/', GalleryView.as_view(), name="galleries-view"),
    url(r'^galleries/(?P<pk>\d+)/$', GalleryDetailView.as_view(), name="gallery-detail"),
    
)
