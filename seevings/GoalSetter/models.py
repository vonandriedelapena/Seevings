from django.db import models

from Account.models import Account


class Goal(models.Model):
    goalId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    targetAmount = models.DecimalField(max_digits=12, decimal_places=2)
    currentAmount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deadline = models.DateField(null=True, blank=True)
    accountGoal = models.ManyToManyField(Account, through='AccountGoal')


class AccountGoal(models.Model):
    accountGoalId = models.AutoField(primary_key=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True)
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, null=True, blank=True)
