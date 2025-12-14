from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list_view, name='transactionList'),

# AJAX Endpoints for CRUD operations
    path('load/', views.load_transactions, name='loadTransactions'),
    path('save/', views.save_transaction, name='saveTransaction'),
    path('<int:pk>/details/', views.get_transaction_details, name='getTransactionDetails'),
    path('<int:pk>/delete/', views.delete_transaction, name='deleteTransaction'),
    path('load-categories/', views.load_categories, name='loadCategories'),
    path('load-goals/', views.load_goals, name='loadGoals'),
    path('load-accounts/', views.load_accounts, name='loadAccounts'),
]
