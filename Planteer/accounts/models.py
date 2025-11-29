from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='accounts/profile_pictures/', default='accounts/profile_pictures/default.avif')
    website = models.URLField(blank=True)

    def __str__(self):
        return f"Profile of {self.user.username}"