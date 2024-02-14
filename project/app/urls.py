
from django.contrib import admin
from django.urls import path, include
from app.views import *

urlpatterns = [
    path('hello/', hello_world, name="hello"),
    path('bot/', chat, name="chat"),
    path('delete-chat/', delete_chat_records, name='delete_chat_records'),
    # path('bot-embedding/', chat_embeddings, name="chat_embeddings"),
]
