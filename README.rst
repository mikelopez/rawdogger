Sciweb Affiliate Galleries (xxx)
================================

Sciweb galleries is used as a pluggable Django application to manage and store 
media galleries from xxx advertisers


Setup
-----
* enable ``'django.template.loaders.eggs.Loader'`` in ``TEMPLATE_LOADERS`` in your ``settings.py`` file.
* Add ``xxxgalleries`` to ``INSTALLED_APPS`` in your ``settings.py`` file.
* Add ``(r'^xxxgalleries/', include('xxxgalleries.urls')),`` to your projects urls.py file
* Add directory to ``STATICFILES_DIRS`` which is by default ``"%s/static" % PROJECT_ROOTDIR,``

Media Files
------------
You can use the media files from demoproject/static

Todo
====
* Local Galleries - Handles storing of image/video files locally and automatically creating the galleries HTML content
* Hosted Galleries - Handles storing of preview images (thumbnails) and stores the targets destination links


