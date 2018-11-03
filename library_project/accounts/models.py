from django.db import models
from django.contrib import auth

# Create your models here.
class User(auth.models.User, auth.models.PermissionsMixin):
    def __str__(self):
        return self.get_full_name()
    
    def __unicode__(self):
        return self.get_full_name()

    
