from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('account/', view_account, name='account'),
    path('account/new/', add_account, name='addAccount'),
    path('account/update/', update_account, name='updateAccount'),
    path('account/close/', close_account, name='closeAccount'),
]
