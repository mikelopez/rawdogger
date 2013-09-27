from django.db import models

class GalleryItem(models.Model):
    name = models.CharField(blank=True, null=True)
    thumb = models.TextField(blank=True, null=True)
    link = models.TextField(blank=True, null=True)
    gallery = models.ForeignKey('Gallery', blank=True, null=True)
    program_type = models.ForeignKey('ProgramTypes', blank=True, null=True)
    description = models.TextField(blank=True, null=True)


class GalleryManager(models.Manager):
    def get_media_by_gallery(self):
        pass

class Gallery(models.Model):
    """ Will consist of a gallery instance
    Whether it be hosted, or local galler
     - if local gallery, overwrite target_link to 
    an internal link since we will be hosting
    the galleries content.
     - if hosted gallery, we log the target link
    and the program type to which the target 
    pertains to
    """
    TYPES = (
            ('local', 'local',),
            ('hosted', 'hosted'),
    )
    objects = GalleryManager()
    name = models.CharField(max_length=30)
    gallery_type = models.CharField(max_length=10, choices=TYPES)
    provider = models.ForeignKey('Providers')

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
    name = models.CharField(max_length=30)
    username = models.CharField(max_length=50, blank=True, null=True)
    password = models.CharField(max_length=20, blank=True, null=True)
    website = models.CharField(blank=True, null=True, max_length=150)
    login_url = models.TextField(blank=True, null=True)
    ccbill = models.CharField(max_length=20, blank=True, null=True)
    notes = models.TextField()

class ProgramTypes(models.Model):
    """ Keep track of the program types for 
    a certain provider. Program types are e.g:
    $35 dollar pps, per signups, per free joins, etc
    """
    provider = models.ForeignKey("Providers")
    name = models.CharField(max_length=15)
    notes = models.TextField(blank=True, null=True)


