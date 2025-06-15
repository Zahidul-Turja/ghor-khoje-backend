from django.contrib import admin
from chat.models import Conversation, Message


# Register your models here.
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "content")


class ConversationAdmin(admin.ModelAdmin):
    list_display = ("user", "other_user", "conversation_type")


admin.site.register(Conversation, ConversationAdmin)
admin.site.register(Message, ChatMessageAdmin)
