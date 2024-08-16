from django.db import models
import uuid


class ChaterSession(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    session = models.ForeignKey(ChaterSession, on_delete=models.CASCADE)
    content = models.TextField()
    is_user = models.BooleanField(default=True)  # True if the message is from the user, False if it's from GPT
    timestamp = models.DateTimeField(auto_now_add=True)