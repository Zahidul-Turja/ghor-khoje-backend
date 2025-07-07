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
    path(
        "messages-by-user-id/<int:user_id>/",
        MessagesByUserIdAPIView.as_view(),
        name="user_messages",
    ),
]
