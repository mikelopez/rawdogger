import os
import urllib
import Image
from random import randint
from datetime import datetime
from termprint import *
from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


MEDIA_ROOT = getattr(settings, "MEDIA_ROOT", "")
DEBUG = getattr(settings, "DEBUG", "")
GALLERY_AUTO_CREATE_MEDIA_FOLDER = getattr(settings, "GALLERY_AUTO_CREATE_MEDIA_FOLDER", False)
LOCAL_TYPE = 'local'
LOCAL_MIXED = 'local-mix'
HOSTED_TYPE = 'hosted'

from resize import *

class GalleryItem(models.Model):
    """
    Thumb can be either local url or remote URL
    depending on the gallery content download type.

    This will be used for local galleries.
    """
    name = models.CharField(max_length=50, blank=True, null=True)
    thumb = models.NullBooleanField(blank=True, null=True)
    filename = models.CharField(blank=True, null=True, max_length=100, default=None)
    link = models.TextField(blank=True, null=True, default=None)
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

    name = models.CharField(max_length=100)
    content = models.CharField(max_length=10, choices=CONTENT, 
                                help_text="Select the type of content",
                                verbose_name="Content Type")
    gallery_type = models.CharField(max_length=10, choices=TYPES)
    media_folder = models.CharField(max_length=100, blank=True, null=True)
    thumb_url = models.TextField(blank=True, null=True, 
                                 verbose_name="Select a thumbnail",
                                 help_text="(Leave empty to manually select)")
    thumb_upload = models.ImageField(upload_to='gallery_thumbs', 
                                     blank=True, null=True,
                                     help_text="Or Upload a thumbnail instead")
    video_url = models.TextField(blank=True, null=True,
                                verbose_name="Video url")
    hosted_jump_link = models.TextField(blank=True, null=True)
    provider = models.ForeignKey('Providers')
    tags = models.ManyToManyField('Tags', blank=True, null=True)
    banners = models.ManyToManyField('Banners', blank=True, null=True)
    filter_name = models.CharField(max_length=50, blank=True, null=True)
    def __str__(self):
        return str(self.name)
    def __unicode__(self):
        return unicode(self.name)

    def get_thumb(self):
        thumb = "thumb.jpg"
        return '<img width="120" height="120" src="/media/galleries/%s/%s" />' % (self.media_folder, thumb)
    get_thumb.allow_tags = True

    @property
    def thumbnail(self):
        """
        First check the gallery item related objects.
        If not found, check the media_folder for any 'thumb.jpg' files
        If not, finally, check self.thumb_url for a remote thumb URL to use.
        """
        for i in self.galleryitem_set.select_related():
            if 'thumb' in getattr(i, 'filename'):
                return "/media/galleries/%s/%s" % (self.media_folder,
                                                  getattr(i, 'filename'))

        if self.get_media_folder():
            if getattr(self, 'content', 'pic') == 'pic':
                if os.path.exists('%s/thumbs/v/thumb.jpg' % (self.get_media_directory())):
                    return "/media/galleries/%s/thumbs/v/thumb.jpg" % (self.media_folder)
            if getattr(self, 'content', 'video') == 'video':
                if os.path.exists('%s/thumbs/h/thumb.jpg' % (self.get_media_directory())):
                    return "/media/galleries/%s/thumbs/h/thumb.jpg" % (self.media_folder)

        if self.thumb_url:
            if "http" in self.thumb_url:
                return self.thumb_url
            return None
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
        """Checks if there is gallery items for each image in this gallery."""
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

    def admin_missing_images(self):
        return self.missing_images
    admin_missing_images.boolean = True

    def admin_media_folder_found(self):
        return self.get_media_folder()
    admin_media_folder_found.boolean = True

    def get_absolute_url(self):
        return reverse('gallery_detail', kwargs={'pk': self.pk})

    def get_media_directory(self):
        """Returns the media directory string for this gallery."""
        return '%sgalleries/%s' % (MEDIA_ROOT, 
                                   getattr(self, 'media_folder'))

    def get_media_folder(self):
        """Checks if the directory is found."""
        return os.path.exists(self.get_media_directory())

    def create_media_folder(self):
        """Creates the media folder"""
        if not self.get_media_folder():
            os.system('mkdir %s' % self.get_media_directory())

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

    def create_thumb_dirs(self):
        """Creates the required thumbnail directories."""
        os.system('mkdir %s/thumbs' % (self.get_media_directory()))
        os.system('mkdir %s/thumbs/v' % (self.get_media_directory()))
        os.system('mkdir %s/thumbs/h' % (self.get_media_directory()))

    def save(self):
        # set filtername if not self.filter_name
        if not getattr(self, 'filter_name', None):
            nm = getattr(self, 'name', '')
            nm = nm.lower().replace(' ', '_')\
                           .replace('#', '--')\
                           .replace('.', '')
            setattr(self, 'filter_name', nm)

        # auto create the media folder only if the settings say so
        if GALLERY_AUTO_CREATE_MEDIA_FOLDER:
            self.create_media_folder()

        # if thumbnail URL exists in field and thumb.jpg does not exist.
        if getattr(self, 'thumb_url', None):
            mdir = self.get_media_directory()
            thumb_dir = "%s/thumbs/thumb.jpg" % (mdir)
            h_thumb_dir = "%s/thumbs/h/thumb.jpg" % (mdir)
            v_thumb_dir = "%s/thumbs/v/thumb.jpg" % (mdir)

            if not os.path.exists('%s/thumbs' % (mdir)):
                self.create_thumb_dirs()

            # if no thumb.jpg file, download the thumb_url
            if not os.path.exists(thumb_dir):
                if not os.path.exists(thumb_dir):
                    urllib.urlretrieve(getattr(self, 'thumb_url'), '%s' % (thumb_dir))
                    # retry without the .mini...
                    if os.path.getsize(thumb_dir) == 0:
                        try:
                            urllib.urlretrieve(str(getattr(self, 'thumb_url')).replace('.mini',''), '%s' % (thumb_dir))
                        except:
                            pass

            # try to resize only if they dont exist
            if self.content == 'pic':
                if not os.path.exists(v_thumb_dir):
                    if os.path.getsize(thumb_dir):
                        try:
                            im = Image.open(thumb_dir)
                            imnew = cropped_thumbnail(im, [250, 300])
                            imnew.save(v_thumb_dir, 'JPEG', quality=100)
                        except:
                            pass
            if self.content == 'video':
                if not os.path.exists(h_thumb_dir):
                    if os.path.getsize(thumb_dir):
                        try:
                            im = Image.open(thumb_dir)
                            imnew = cropped_thumbnail(im, [320, 220])
                            imnew.save(h_thumb_dir, 'JPEG', quality=100)
                        except:
                            pass

        super(Gallery, self).save()


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
    cache_picgalleries_count = models.IntegerField(default=0)
    cache_vidgalleries_count = models.IntegerField(default=0)
    main_tag = models.NullBooleanField(default=False)
    site_tag = models.NullBooleanField(default=False)
    model_tag = models.NullBooleanField(default=False)
    @property
    def count_pic_galleries(self):
        """Returns count of related galleries"""
        c =  self.gallery_set.filter(content='pic').count()
        self.cache_picgalleries_count = c
        self.save()
        return c
    @property
    def count_video_galleries(self):
        """Returns count of related galleries"""
        c = self.gallery_set.filter(content='video').count()
        self.cache_vidgalleries_count = c
        self.save()
        return c

    def update_vid_thumb(self):
        """Return the video thumbnail"""
        return None

    @property
    def update_pic_thumb(self, try_video=False):
        """Updates the picture thumbnail gallery to use for 
        the front face of the tag catgegory when using a 
        picture gallery to represent it."""
        try:
            counts = self.gallery_set.filter(content='pic').count()
            rands = 0
            if counts > 0:
                try:
                    rands = randint(0, (counts-1))
                except:
                    pass
            thmb = self.gallery_set.filter(content='pic')[rands]

            try:
                obj = PicTagFaces.objects.get(tag=self)
                obj.gallery = thmb                
            except PicTagFaces.DoesNotExist:
                obj = PicTagFaces(gallery=thmb, tag=self)
            obj.save()
        except (IndexError, AttributeError):
            pass

    def get_pic_tag_thumb(self):
        """Returns the tag face gallery"""
        try:
            return PicTagFaces.objects.get(tag=self).gallery_thumb
        except (PicTagFaces.DoesNotExist, AttributeError):
            return "#"

    def __str__(self):
        return str(self.name)
    def __unicode__(self):
        return unicode(self.name)


class Banners(models.Model):
    """Banners"""
    TYPES = (('horizontal', 'horizontal'),
             ('vertical', 'vertical'),
             ('square', 'square'))
    name = models.CharField(max_length=50)
    ratio = models.CharField(max_length=20, choices=TYPES)
    jumplink = models.TextField()
    picture = models.TextField()
    width = models.IntegerField(blank=True, null=True, default=0)
    height = models.IntegerField(blank=True, null=True, default=0)
    provider = models.ForeignKey('Providers')
    def __str__(self):
        return str(self.name)
    def __unicode__(self):
        return unicode(self.name)
    def get_absolute_url(self):
        return reverse('banners_detail', kwargs={'pk': self.pk})
    def count_galleries(self):
        """Returns count of related galleries"""
        return self.gallery_set.all().count()


class PicTagFaces(models.Model):
    """
    Contains the gallery reference for a main tag.
    """
    gallery = models.ForeignKey('Gallery')
    tag = models.ForeignKey('Tags')
    gallery_thumb = models.TextField(blank=True, null=True)
    def save(self):
        self.gallery_thumb = self.gallery.thumbnail
        super(PicTagFaces, self).save()

class VidTagFaces(models.Model):
    """
    Contains the gallery reference for a main tag.
    """
    gallery = models.ForeignKey('Gallery')
    tag = models.ForeignKey('Tags')
    gallery_thumb = models.TextField(blank=True, null=True)
    def save(self):
        self.gallery_thumb = self.gallery.thumbnail
        super(PicTagFaces, self).save()