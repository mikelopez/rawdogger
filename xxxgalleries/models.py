from django.db import models

class GalleryItem(models.Model):
    """
    Thumb can be either local url or remote URL
    depending on the gallery content download type.

    This will be used for local galleries.
    """
    name = models.CharField(blank=True, null=True)
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
            ('local', 'local',),
            ('hosted', 'hosted'),
    )
    name = models.CharField(max_length=30)
    gallery_type = models.CharField(max_length=10, choices=TYPES)
    hosted_jump_link = models.TextField(blank=True, null=True)
    provider = models.ForeignKey('Providers')
    @property
    def link(self):
        if self.gallery_type == 'local':
            return "/galleries/%s" % getattr(self, "id")
        if self.gallery_type == "hosted":
            return getattr(self, "hosted_jump_link")
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


