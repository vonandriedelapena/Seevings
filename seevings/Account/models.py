from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)
    birthDate = models.DateField(null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['birthDate', 'first_name', 'last_name']

class Account(models.Model):
    accountId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=120, null=False)
    balance = models.FloatField(default=0, null=False)
    createdAt = models.CharField(max_length=120, null=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

