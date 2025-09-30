from django.db import models


# Create your models here.
class User(models.Model):
    userId = models.AutoField(primary_key=True)
    email = models.CharField(max_length=120, null=False)
    password = models.CharField(max_length=120, null=False)
    firstName = models.CharField(max_length=120, null=False)
    lastName = models.CharField(max_length=120, null=False)
    birthDate = models.DateField(null=False)


class Account(models.Model):
    accountId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=120, null=False)
    balance = models.FloatField(default=0, null=False)
    createdAt = models.CharField(max_length=120, null=False)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
