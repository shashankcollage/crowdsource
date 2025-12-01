from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('',views.admin_login,name="admin-panel"),
    path('dashboard/', views.dashboard, name='dashboard'),
]

