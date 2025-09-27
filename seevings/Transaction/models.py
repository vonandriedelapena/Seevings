from django.db import models

from Account.models import Account


class Transaction(models.Model):
    transactionId = models.AutoField(primary_key=True)
    accountId = models.ForeignKey(Account, on_delete=models.RESTRICT)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=False)
    timestamp = models.DateTimeField(null=False)
    notes = models.CharField(max_length=120, null=False)
    type_trans = (('T', 'Transfer'), ('E', 'Expense'), ('I', 'Income'), ('S', 'Saving'))
    type = models.CharField(max_length=1, choices=type_trans, default='E')

    def __str__(self):
        return self.type_trans + ': $' + self.amount + ' (' + self.notes + ': ' + self.timestamp + ')'


class Transfer(Transaction):
    receiverId = models.ForeignKey(Account, on_delete=models.RESTRICT)


class Category(models.Model):
    categoryId = models.AutoField(primary_key=True)
    name = models.CharField(max_length=120, null=False)
    description = models.CharField(max_length=120, null=False)


class Expense(Transaction):
    categoryId = models.ForeignKey(Category, on_delete=models.RESTRICT)
    name = models.CharField(max_length=120, null=False)


class Income(Transaction):
    source = models.CharField(max_length=120, null=False)


class Saving(Transaction):
    goalId = models.AutoField(primary_key=True)  # TODO: CHANGE THIS TO FOREIGN KEY FROM GOAL ENTITY
