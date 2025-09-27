from django.db import models

from Account.models import Account

# Create your models here.
class Budget(models.Model):
    budgetId = models.AutoField(primary_key=True)
    accountId = models.ForeignKey(Account, on_delete=models.RESTRICT)
    frequency = models.IntegerField(null=False)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=False)
    startDate = models.DateField(null=False)
    endDate = models.DateField(null=False)

