from django.contrib import admin
from django.urls import path
from .import views

urlpatterns = [
  path('/front_page',views.dashboard,name="dashboard"),
  path('',views.dashboard_view,name="dashboard_view"),
  path('/dash',views.dash,name="dash")
]
