"""URL configuration for vault app."""
from django.urls import path
from . import views

app_name = 'vault'

urlpatterns = [
    path('', views.vault_list, name='list'),
    path('resources/', views.VaultListView.as_view(), name='resources'),
]
