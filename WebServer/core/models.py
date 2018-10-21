from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, AbstractUser


class CommonModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser (AbstractUser):
    USERNAME_FIELD = 'username'
    facebook_id = models.IntegerField( null=True, blank=True)
    facebook_token = models.CharField(max_length=50, null=True, blank=True)
    avatar = models.ImageField('image', null=True, blank=True, upload_to='img')

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
