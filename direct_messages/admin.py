from django.contrib import admin
from .models import Message, ChatRoom

@admin.register(ChatRoom)
class RoomAdmin(admin.ModelAdmin):
    pass

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):

    list_display = (
        "text",
        "user",
        "room",
        "created_at",
    )

    list_filter = ("created_at", )