import os
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
MEDIA_ROOT = getattr(settings, "MEDIA_ROOT", "")

LOCAL_TYPE = 'local'
LOCAL_MIXED = 'local-mix'
HOSTED_TYPE = 'hosted'

class GalleryItem(models.Model):
    """
    Thumb can be either local url or remote URL
    depending on the gallery content download type.

    This will be used for local galleries.
    """
    name = models.CharField(max_length=50, blank=True, null=True)
    thumb = models.TextField(blank=True, null=True)
    filename = models.CharField(blank=True, null=True, max_length=100)
    link = models.TextField(blank=True, null=True)
    gallery = models.ForeignKey('Gallery', blank=True, null=True)
    program_type = models.ForeignKey('ProgramTypes', blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class Gallery(models.Model):
    """ Will consist of a gallery instance
    Whether it be hosted, or local gallery.
    Hosted galleries automatically redirect to the
    URL specified.
    Local galleries will display the items from
    GalleryItems in an internal URL.
    """
    TYPES = (
            (LOCAL_TYPE, LOCAL_TYPE),
            (LOCAL_MIXED, LOCAL_MIXED),
            (HOSTED_TYPE, HOSTED_TYPE),
    )
    CONTENT = (
            ('pic', 'pic'),
            ('video', 'video'),
            ('both', 'both'))

    name = models.CharField(max_length=30)
    gallery_type = models.CharField(max_length=10, choices=TYPES)
    media_folder = models.CharField(max_length=100, blank=True, null=True)
    thumb_url = models.TextField(blank=True, null=True, 
                                    verbose_name="Select a thumbnail",
                                    help_text="(Leave empty to manually select)")
    thumb_upload = models.ImageField(upload_to='gallery_thumbs', 
                                     blank=True, null=True,
                                     help_text="Or Upload a thumbnail instead")
    hosted_jump_link = models.TextField(blank=True, null=True)
    provider = models.ForeignKey('Providers')
    tags = models.ManyToManyField('Tags', blank=True, null=True)
    @property
    def thumbnail(self):
        for i in self.galleryitem_set.select_related():
            if 'thumb' in getattr(i, 'filename'):
                return getattr(i, 'filename')
        for i in self.show_media():
            if 'thumb' in i:
                return i
        return None

    @property
    def link(self):
        if self.gallery_type == LOCAL_TYPE:
            return "%s%s" % (reverse('gallery_detail'), getattr(self, "id"))
        if self.gallery_type == HOSTED_TYPE:
            return getattr(self, "hosted_jump_link")
        return None

    @property
    def is_sync(self):
        """Checks if theere is gallery items for each image in this gallery."""
        items = self.galleryitem_set.select_related()
        if not items:
            return False
        return self.images_sync_db

    @property
    def images_sync_db(self):
        """Checks if there are no additional images added later to the 
        folder which have not been added to the galleryItems, would need
        to run a resync if this is off."""
        items_append = []
        for i in items:
            items_check.append(i)
        for i in self.show_media():
            if not i in items_append:
                return False
        return True

    @property
    def missing_images(self):
        """Checks if there is items in GalleryItem."""
        images = self.show_media()
        if not images:
            return True
        result = False
        for i in self.galleryitem_set.select_related():
            # if entry in galleryitem does not exist in filesystem
            if not i in images:
                result = True
        return result

    def get_absolute_url(self):
        return reverse('gallery_detail', kwargs={'pk': self.pk})

    def get_media_directory(self):
        """Returns the media directory string for this gallery."""
        return '%s/galleries/%s' % (MEDIA_ROOT, 
                                   getattr(self, 'media_folder'))

    def get_media_folder(self):
        """Checks if the directory is found."""
        return os.path.exists(self.get_media_directory())

    def show_media(self):
        """Showa the media if the gallery is local"""
        if getattr(self, 'gallery_type') == LOCAL_TYPE or \
                getattr(self, 'gallery_type') == LOCAL_MIXED:
            media_dir = '%s/galleries/%s' % (MEDIA_ROOT, self.media_folder)
            if not os.path.exists(media_dir):
                return None
            files = []
            for filename in os.listdir(media_dir):
                for k in ['.jpg', '.gif', 'wmv', 'mp4', '.png']:
                    if k in filename.lower():
                        files.append(filename)
            return files
        return None


class Providers(models.Model):
    """ Lets keep track of the providers that
    we will be dealing with.
     - name
     - username
     - password
     - website (optional)
     - login url (optional)
     - ccbill (optional)
     - notes
    """
    def __str__(self):
        return str("%s / %s" % (self.name, self.website))
    def __unicode__(self):
        return unicode("%s / %s" % (self.name, self.website))

    def get_absolute_url(self):
        return reverse('provider_detail', kwargs={'pk': self.pk})

    name = models.CharField(max_length=30)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(blank=True, null=True, max_length=150)
    login_url = models.CharField(max_length=200, blank=True, null=True)
    ccbill = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    logo = models.TextField(blank=True, null=True)

class ProgramTypes(models.Model):
    """ Keep track of the program types for 
    a certain provider. Program types are e.g:
    $35 dollar pps, per signups, per free joins, etc
    """
    provider = models.ForeignKey("Providers")
    name = models.CharField(max_length=15)
    notes = models.TextField(blank=True, null=True)

class Tags(models.Model):
    """Hashtag or categorize a gallery"""
    name = models.CharField(max_length=50)
