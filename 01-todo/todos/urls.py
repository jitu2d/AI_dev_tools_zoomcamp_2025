from django.urls import path
from . import views

urlpatterns = [
    path('', views.task_list, name='task_list'),
    path('create/', views.task_create, name='task_create'),
    path('edit/<int:task_id>/', views.task_edit, name='task_edit'),
    path('delete/<int:task_id>/', views.task_delete, name='task_delete'),
    path('toggle/<int:task_id>/', views.task_toggle_resolve, name='task_toggle_resolve'),
    path('calendar/', views.calendar_view, name='calendar_view'),
]
