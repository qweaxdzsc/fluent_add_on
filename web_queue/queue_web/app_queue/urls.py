from django.urls import path
from . import views

app_name = 'app_queue'

urlpatterns = [
    path(r'', views.index),
    path(r'add/', views.add_project),
    path(r'history/', views.view_history),
    path(r'setting/', views.setting),
]

