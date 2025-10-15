from django.urls import path
from . import views

app_name = 'realtime_chat'

# urlpatterns = [
#     path('', views.chat_list, name='chat_list'),
#     path('messages/<int:user_id>/', views.get_messages, name='get_messages'),
#     path('send/<int:user_id>/', views.send_message, name='send_message'),
#     path('mark_seen/<int:user_id>/', views.mark_seen, name='mark_seen'), 

# ]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_list, name='chat_list'),
    path('messages/<int:user_id>/', views.get_messages, name='get_messages'),
    path('send/<int:user_id>/', views.send_message, name='send_message'),
    path('mark_seen/<int:user_id>/', views.mark_seen, name='mark_seen'),
    path('typing/<int:user_id>/', views.typing_status, name='typing'),
    path('typing_status/<int:user_id>/', views.get_typing_status, name='get_typing_status'),
]

