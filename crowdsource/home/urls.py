from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
  path('front_page/',views.dashboard,name="dashboard"),
  path('',views.dashboard_view,name="dashboard_view"),
  path('dash/',views.dash,name="dash"),
  path('dashboard', views.user_management, name='user_management'),
  path('users/', views.UserManagementView.as_view(), name='user_management'),
  path('users/add-ajax/', views.add_user_ajax, name='add_user_ajax'),
]
