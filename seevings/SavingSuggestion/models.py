from django.db import models

from Transaction.models import Expense


class SavingSuggestion(models.Model):
    expenseId = models.ForeignKey(Expense, on_delete=models.CASCADE)
    suggestionId = models.AutoField(primary_key=True)
    potentialSaving = models.DecimalField(decimal_places=2, max_digits=10)
    recommendationText = models.CharField(max_length=120, null=False)

    def __str__(self):
        return f"Save {self.potentialSaving}: {self.recommendationText}"
