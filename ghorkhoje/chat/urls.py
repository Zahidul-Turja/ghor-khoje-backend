from django.urls import path

from chat.views import *

chat_urlpatterns = [
    path(
        "conversations/",
        AllConversationsAPIView.as_view(),
        name="all_conversations",
    ),
    path(
        "messages/<str:conversation_id>/",
        AllMessagesAPIView.as_view(),
        name="all_messages",
    ),
]
