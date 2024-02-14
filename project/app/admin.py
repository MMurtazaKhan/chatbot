from django.contrib import admin
from .models import ChatBot

@admin.register(ChatBot)
class ChatBotAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'role', 'content']  # Customize the displayed fields in the admin list view
    search_fields = ['user_id', 'role']  # Add fields you want to be searchable in the admin

    # You can customize other options, filters, etc., based on your requirements.
