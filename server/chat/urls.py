from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('join-room/', views.join_room, name='join-room'),
    path('post-message/', views.post_message, name='post-message'),
    path('get-messages/', views.get_messages, name='get-messages'),
]
