from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.conf import settings
from django.contrib.auth.models import AbstractUser
#User = get_user_model
# class User(AbstractUser):
#     image = models.ImageField(upload_to='myimages')
class profile(models.Model):
    
    name = models.CharField(max_length = 30,default = "name")
    domain  = models.CharField(max_length = 30)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    bio = models.TextField(max_length= 100)
    image = models.ImageField(upload_to  = 'profile/')

