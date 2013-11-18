from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings
MEDIA_ROOT = getattr(settings, "MEDIA_ROOT", "")

LOCAL_TYPE = 'local'
HOSTED_TYPE = 'hosted'

class GalleryItem(models.Model):
    """
    Thumb can be either local url or remote URL
    depending on the gallery content download type.

    This will be used for local galleries.
    """
    name = models.CharField(max_length=50, blank=True, null=True)
    thumb = models.TextField(blank=True, null=True)
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
            (HOSTED_TYPE, HOSTED_TYPE),
    )
    name = models.CharField(max_length=30)
    gallery_type = models.CharField(max_length=10, choices=TYPES)
    media_folder = mod
    thumb_url = models.TextField(blank=True, null=True, 
                                    verbose_name="Select a thumbnail")
    thumb_upload = models.ImageField(upload_to='gallery_thumbs', blank=True, null=True,
                                     help_text="Upload a thumbnail instead")
    hosted_jump_link = models.TextField(blank=True, null=True)
    provider = models.ForeignKey('Providers')
    @property
    def link(self):
        if self.gallery_type == LOCAL_TYPE:
            return "%s%s" % (reverse('gallery_detail'), getattr(self, "id"))
        if self.gallery_type == HOSTED_TYPE:
            return getattr(self, "hosted_jump_link")
        return None

    def show_media(self):
        """Showa the media if the gallery is local"""
        if getattr(self, 'gallery_type') == LOCAL_TYPE:
            media_dir = '%s/galleries/%s', (MEDIA_ROOT, self.media_folder)
            if not os.path.exists(media_dir):
                return None
            files = []
            for filename in os.listdir(media_dir):
                for k in ['.jpg', '.gif', 'wmv', 'mp4']:
                    if k in filename.lower():
                        files.append(i)
            return files


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
    def get_absolute_url(self):
        return reverse('provider_detail', kwargs={'pk': self.pk})

    name = models.CharField(max_length=30)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(blank=True, null=True, max_length=150)
    login_url = models.CharField(max_length=200, blank=True, null=True)
    ccbill = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

class ProgramTypes(models.Model):
    """ Keep track of the program types for 
    a certain provider. Program types are e.g:
    $35 dollar pps, per signups, per free joins, etc
    """
    provider = models.ForeignKey("Providers")
    name = models.CharField(max_length=15)
    notes = models.TextField(blank=True, null=True)


