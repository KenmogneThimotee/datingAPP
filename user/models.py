from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

SEX_CHOICES = (
    ('F', 'Female',),
    ('M', 'Male',),
)

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

    likes = models.ManyToManyField(to="self", through='Likes')
    dislikes = models.ManyToManyField(to='self', through='Dislikes')
    
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, db_index=True, default='M')
    preferred_sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='F')

    preferred_age_min = models.IntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(130)], default=18)
    preferred_age_max = models.IntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(130)], default=130)
    
    last_location = models.PointField(max_length=40, null=True)
    preferred_radius = models.IntegerField(default=5,
                                           help_text="in kilometers")
    
    objects = UserManager()
    ordering = ('email',)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Likes(models.Model):
    
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="initial_user")
    liked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="liked_user")
    
class Dislikes(models.Model):
    
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dislike_initial_user")
    disliked = models.ForeignKey(User, on_delete=models.CASCADE, related_name="disliked_user")
    
class Match(models.Model):
    
    date = models.DateTimeField(auto_now_add=True)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user2')