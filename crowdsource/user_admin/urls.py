from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
    path('',views.admin_login,name="admin-panel"),
    path('admin-panel/',views.admin_login,name="admin-panel"),
    path('admin-logout/',views.admin_logout, name='admin-logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('demo/', views.demo, name='demo'),
]

