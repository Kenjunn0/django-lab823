from django.db import models
from common.models import CommonModel

class ChatRoom(CommonModel):

    """room model definition"""

    users = models.ManyToManyField("users.User", )

    def __str__(self):
        return "Chatting Room"


class Message(CommonModel):

    """message model definition"""

    text = models.TextField()
    user = models.ForeignKey("users.User", on_delete=models.SET_NULL, null=True, blank=True, related_name="messages", )
    room = models.ForeignKey("direct_messages.ChatRoom", on_delete=models.CASCADE, related_name="messages", )

    def __str__(self):
        return f"{self.user} says: {self.text}"