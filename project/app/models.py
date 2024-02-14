from django.db import models

# Create your models here.
class ChatBot(models.Model):
    user_id = models.IntegerField(null=False)
    role = models.CharField(max_length=10, null=False)
    content = models.TextField(null=False)