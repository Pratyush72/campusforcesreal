from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('notes/', views.notes, name='notes'),
    path('upload-notes/', views.upload_notes, name='upload_notes'),
    path('live-projects/', views.live_projects, name='live_projects'),
    path('profile/', views.profile, name='profile'),
    path('resume-builder/', views.resume_builder, name='resume_builder'),
    path('membership/', views.membership, name='membership'),
]
