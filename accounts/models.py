from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
# ----------------------------------------------


class User(AbstractUser):
    id_mfa_enabled = models.BooleanField(default=False)
    department = models.CharField(max_length = 100, blank = True, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    
    
    # define the string representation of the model for better readability in the admin interface and other contexts 
    # ----------------------------------------------
    def __str__(self):
        return self.username