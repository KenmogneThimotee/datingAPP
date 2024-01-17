from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):
    # Define your custom fields here
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    first_name = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    date_of_bith = models.DateField(null=True, blank=True)
    
    validated = models.BooleanField(default=False)
    validation_code = models.CharField(max_length=5, null=True)
    
    reset_code = models.CharField(max_length=5, null=True)
    reset_code_validated = models.BooleanField(default=False)
    
    objects = UserManager()


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
