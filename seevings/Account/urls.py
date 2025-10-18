from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('', register, name='register'),
    path('login/', login, name='login'),
]