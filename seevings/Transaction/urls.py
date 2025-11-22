from django.urls import path
from . import views

urlpatterns = [
    path('', views.transaction_list, name='transactionList'),

# AJAX Endpoints for CRUD operations
    path('transaction/save/', views.save_transaction, name='saveTransaction'),
    path('transaction/<int:pk>/details/', views.get_transaction_details, name='getTransactionDetails'),
    path('transaction/<int:pk>/delete/', views.delete_transaction, name='deleteTransaction'),
]
