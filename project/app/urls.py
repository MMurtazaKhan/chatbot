
from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    path('hello/', hello_world, name="hello"),
    path('bot/', chat, name="chat"),
    path('delete-chat/', delete_chat_records, name='delete_chat_records'),
    path('chat-history/', chat_history, name='chat_history'),
    path('carbon-reduction/', carbon_reduction, name='chat-reduction'),
    
]
