from django.urls import path
from django.contrib.auth import views as auth_views

from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', next_page='../account/'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='../login/'), name='logout'),
    path('account/', view_account, name='account'),
    path('account/detailed/', view_detailed, name='accountDetailed'),
    path('account/new/', add_account, name='addAccount'),
    path('account/update/', update_account, name='updateAccount'),
    path('account/close/', close_account, name='closeAccount'),
    path('user/', view_user, name='user'),
]
