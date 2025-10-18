from django.contrib import admin

from .models import Goal, AccountGoal
# Register your models here.
admin.site.register(Goal)
admin.site.register(AccountGoal)
