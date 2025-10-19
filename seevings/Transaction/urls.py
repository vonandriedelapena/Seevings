from django.urls import path
from . import views

urlpatterns = [
    path('transactions/', views.transaction_list, name='transactionList'),
    path('transaction/create/', views.create_transaction, name='createTransaction'),

    path('transaction/transfer/add/', views.add_transfer, name='addTransfer'),
    path('transaction/transfer/list/', views.transfer_list, name='transferList'),

    path('transaction/expense/add/', views.add_expense, name='addExpense'),
    path('transaction/expense/list/', views.expense_list, name='expenseList'),

    path('transaction/income/add/', views.add_income, name='addIncome'),
    path('transaction/income/list/', views.income_list, name='incomeList'),

    path('transaction/saving/add/', views.add_saving, name='addSaving'),
    path('transaction/saving/list/', views.saving_list, name='savingList'),
]
