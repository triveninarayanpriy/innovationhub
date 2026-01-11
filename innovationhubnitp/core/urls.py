"""URL configuration for core app."""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('apply-mentor/', views.apply_mentor, name='apply_mentor'),
    path('send-inquiry/', views.send_inquiry, name='send_inquiry'),
]
