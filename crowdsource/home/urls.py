from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
  path('dashboard/',views.dashboard,name="dashboard"),
  path('',views.dashboard_view,name="dashboard_view"),


]
