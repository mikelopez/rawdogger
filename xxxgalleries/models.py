from django.db import models

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
    pass

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
    pass

class ProgramTypes(models.Model):
    """ Keep track of the program types for 
    a certain provider. Program types are e.g:
    $35 dollar pps, per signups, per free joins, etc
    """
    provider = models.ForeignKey("Providers")

