from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if not extra_fields.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True.'))
        if not extra_fields.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)


# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique=True)
    birthDate = models.DateField(null=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['birthDate', 'first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Account(models.Model):
    accountId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, null=False)
    balance = models.FloatField(default=0, null=False)
    createdAt = models.DateTimeField(max_length=120, null=False)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
