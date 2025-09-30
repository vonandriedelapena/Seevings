from django.contrib import admin

from .apps import TransactionConfig
from .models import *

# Register your models here.
admin.site.register(Transaction)
admin.site.register(Transfer)
admin.site.register(Category)
admin.site.register(Saving)
admin.site.register(Expense)
admin.site.register(Income)
