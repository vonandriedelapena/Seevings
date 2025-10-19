from django.urls import path
from . import views

urlpatterns = [
    path('goals/', views.goal_list_view, name='goal_list'),
    path('set_goal/', views.set_goal_view, name='set_goal'),
    path('edit_goal/', views.edit_goal_view, name='edit_goal'),
]
