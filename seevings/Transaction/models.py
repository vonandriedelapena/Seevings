from django.db import models
from Account.models import Account
from GoalSetter.models import Goal


class Transaction(models.Model):
    transactionId = models.AutoField(primary_key=True)
    accountId = models.ForeignKey(Account, on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=False)
    timestamp = models.DateTimeField(null=False)
    notes = models.CharField(max_length=120, null=False)
    type_trans = (('T', 'Transfer'), ('E', 'Expense'), ('I', 'Income'), ('S', 'Saving'))
    type = models.CharField(max_length=1, choices=type_trans, default='I')

    def __str__(self):
        return f"{self.get_type_display()}: ${self.amount} ({self.notes} at {self.timestamp})"

    def get_subclass_instance(self):
        if self.type == 'T':
            return Transfer.objects.get(pk=self.pk)
        elif self.type == 'E':
            return Expense.objects.get(pk=self.pk)
        elif self.type == 'I':
            return Income.objects.get(pk=self.pk)
        else:
            return Saving.objects.get(pk=self.pk)


class Transfer(Transaction):
    receiverId = models.CharField(max_length=64, null=False)
#   Removed FK because this is only a tracker app
#   Different users cannot interact

class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, null=False)
    description = models.CharField(max_length=120, null=False)

    def __str__(self):
        return self.name


class Expense(Transaction):
    categoryId = models.ForeignKey(Category, on_delete=models.RESTRICT)
    name = models.CharField(max_length=120, null=False)


class Income(Transaction):
    source = models.CharField(max_length=120, null=False)


class Saving(Transaction):
    goalId = models.ForeignKey(Goal, on_delete=models.CASCADE)

