from django.urls import path
from . import views

app_name = "careers"

urlpatterns = [
    path('', views.career_list, name='career_list'),
    path('<int:pk>/', views.career_detail, name='career_detail'),
    path('my-applications/', views.my_applications, name='my_applications'),
    path('resume/<int:pk>/', views.view_resume, name='view_resume'),

]
