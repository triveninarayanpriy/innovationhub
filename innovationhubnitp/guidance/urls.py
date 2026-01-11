"""URL routes for the Senior Guidance portal."""
from django.urls import path
from . import views

app_name = 'guidance'

urlpatterns = [
    path('', views.guidance_view, name='guidance_home'),
    path('request/<int:mentor_id>/', views.request_guidance, name='request_guidance'),
    path('dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    path('chat/<int:request_id>/', views.chat_view, name='chat'),
]
