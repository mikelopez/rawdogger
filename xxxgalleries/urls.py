from django.conf.urls import patterns, include, url
from django.conf import settings

from xxxgalleries.views import IndexView, \
        GalleryView, GalleryDetailView, CreateGallery, UpdateGallery, \
        CreateProvider, UpdateProvider, ProviderView, ProviderDetailView, \
        TagsView, TagsDetailView, AddTagToGallery, RemoveTagFromGallery, \
        CreateBanners, UpdateBanners, BannersView, BannersDetailView, \
        SetTagType, RemoveTagType, CreateProviderAccounts, UpdateProviderAccounts, \
        ProviderAccountsView, ProviderAccountsDetailView, \
        CreateProviderWebsites, UpdateProviderWebsites, ProviderWebsitesView, ProviderWebsitesDetailView, \
        CreateProviderWebsites, UpdateProviderWebsiteLinks, ProviderWebsiteLinksView, ProviderWebsiteLinksDetailView, \
        CreateProgramTypes, UpdateProgramTypes, ProgramTypesView, ProgramTypesDetailView

        

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name="xxx_index"),
    url(r'^gallery/add', CreateGallery.as_view(), name="galleries_add"),
    url(r'^gallery/update/(?P<pk>\d+)/$', UpdateGallery.as_view(), name="galleries_update"),
    url(r'^gallery/', GalleryView.as_view(), name="galleries_view"),
    url(r'^galleries/(?P<pk>\d+)/$', GalleryDetailView.as_view(), name="gallery_detail"),

    url(r'^provider_accounts/add', CreateProviderAccounts.as_view(), name="provider_accounts_add"),
    url(r'^provider_accounts/update/(?P<pk>\d+)/$', UpdateProviderAccounts.as_view(), name="provider_accounts_update"),
    url(r'^provider_accounts/(?P<pk>\d+)/$', ProviderAccountsDetailView.as_view(), name="provider_accounts_detail"),
    url(r'^provider_accounts/', ProviderAccountsView.as_view(), name="provider_accounts_view"),
    

    url(r'^provider_websites/add', CreateProviderWebsites.as_view(), name="provider_websites_add"),
    url(r'^provider_websites/update/(?P<pk>\d+)/$', UpdateProviderWebsites.as_view(), name="provider_websites_update"),
    url(r'^provider_websites/(?P<pk>\d+)/$', ProviderWebsitesDetailView.as_view(), name="provider_websites_detail"),
    url(r'^provider_websites/', ProviderWebsitesView.as_view(), name="provider_websites_view"),
    

    url(r'^provider_websitelinks/add', CreateProviderWebsites.as_view(), name="provider_websitelinks_add"),
    url(r'^provider_websitelinks/update/(?P<pk>\d+)/$', UpdateProviderWebsiteLinks.as_view(), name="provider_websitelinks_update"),
    url(r'^provider_websitelinks/(?P<pk>\d+)/$', ProviderWebsiteLinksDetailView.as_view(), name="provider_websitelinks_detail"),
    url(r'^provider_websitelinks/', ProviderWebsiteLinksView.as_view(), name="provider_websitelinks_view"),
    

    url(r'^provider/add', CreateProvider.as_view(), name="providers_add"),
    url(r'^provider/update/(?P<pk>\d+)/$', UpdateProvider.as_view(), name="providers_update"),
    url(r'^providers/(?P<pk>\d+)/$', ProviderDetailView.as_view(), name="provider_detail"),
    url(r'^provider/', ProviderView.as_view(), name="providers_view"),
    

    url(r'^program_types/add', CreateProgramTypes.as_view(), name="program_types_add"),
    url(r'^program_types/update/(?P<pk>\d+)/$', UpdateProgramTypes.as_view(), name="program_types_update"),
    url(r'^program_types/(?P<pk>\d+)/$', ProgramTypesDetailView.as_view(), name="program_types_detail"),
    url(r'^program_types/', ProgramTypesView.as_view(), name="program_types_view"),
    

    url(r'^banners/add', CreateBanners.as_view(), name="banners_add"),
    url(r'^banners/update/(?P<pk>\d+)/$', UpdateBanners.as_view(), name="banners_update"),
    url(r'^banners/(?P<pk>\d+)/$', BannersDetailView.as_view(), name="banners_detail"),
    url(r'^banners/', BannersView.as_view(), name="banners_view"),
    
    
    url(r'^remtagtype/', RemoveTagType.as_view(), name="remove_tag_type"),
    url(r'^tagtype/', SetTagType.as_view(), name="set_tag_type"),
    url(r'^tag/(?P<pk>\d+)/$', TagsDetailView.as_view(), name="tags_detail"),
    url(r'^tags/', TagsView.as_view(), name="tags_view"),
    url(r'^addtag/', AddTagToGallery.as_view(), name="addtag"),
    url(r'^deltag/', RemoveTagFromGallery.as_view(), name="deltag"),
)
