# admin_panel/urls.py
from django.urls import path
from . import views
# admin_panel/views.py


app_name = 'admin_panel'

urlpatterns = [
    # auth
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),

    # dashboard
    path('', views.dashboard, name='dashboard'),
    path('users/', views.manage_users, name='manage_users'),
    path('edit-user/<int:user_id>/', views.edit_user, name='edit_user'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),



 
    # Projects (CRUD)
    path('projects/', views.manage_projects, name='manage_projects'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/edit/<int:pk>/', views.edit_project, name='edit_project'),
    path('projects/delete/<int:pk>/', views.delete_project, name='delete_project'),

   
    # LiveWork
    path('livework/', views.manage_livework, name='manage_livework'),
    path('livework/add/', views.add_livework, name='add_livework'),  # <-- ye line sabse important
    path('livework/edit/<int:pk>/', views.edit_livework, name='edit_livework'),
    path('livework/delete/<int:pk>/', views.delete_livework, name='delete_livework'),

    # Job Applications (view / change status)
    path('jobs/', views.manage_jobs, name='manage_jobs'),
    path('jobs/status/<int:pk>/', views.update_job_status, name='update_job_status'),  # expects POST with 'status'
    path('jobs/download_resume/<int:pk>/', views.download_resume, name='download_resume'),
]
