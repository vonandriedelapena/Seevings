from django.urls import path

from .views import *

urlpatterns = [
    path('budgets/', budget_list, name='budgetList'),
    path('budget/add/', add_budget, name='addBudget'),
    path('budget/update/', update_budget, name='updateBudget'),
    path('budget/remove/', remove_budget, name='removeBudget')
]