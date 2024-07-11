from django.db import models

# Create your models here.
class ChatBot(models.Model):
    user_id = models.CharField(max_length=100, null=False)
    role = models.CharField(max_length=10, null=False)
    content = models.TextField(null=False)