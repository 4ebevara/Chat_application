from django.db import models
from django.contrib.auth.models import User

class Chat(models.Model):
    is_group = models.BooleanField(default=False)
    name = models.CharField(max_length=255, blank=True)
    participants = models.ManyToManyField(User, related_name='chats')

    def __str__(self):
        return self.name if self.is_group else f"Chat {self.id}"

class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.username}: {self.content[:20]}"