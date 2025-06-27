import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from django.db.models import Q

from chat.models import Conversation, Message
from user.models import User

# from chat_app.services import *


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        # Check if user is authenticated
        print(self.scope)
        if not self.scope["user"]:
            self.close()
            return

        self.user = self.scope["user"]
        self.is_admin = self.scope.get("is_admin", False)

        # Accept the connection
        self.accept()

        # Join user to their personal room for notifications
        self.personal_room = f"user_{self.user.id}"
        async_to_sync(self.channel_layer.group_add)(
            self.personal_room, self.channel_name
        )

        # Join admin room if user is admin for customer support
        if self.is_admin:
            self.admin_room = "admin_support"
            async_to_sync(self.channel_layer.group_add)(
                self.admin_room, self.channel_name
            )

        print(f"User {self.user} connected")

    def disconnect(self, close_code):
        # Leave personal room
        async_to_sync(self.channel_layer.group_discard)(
            self.personal_room, self.channel_name
        )

        # Leave admin room if admin
        if self.is_admin:
            async_to_sync(self.channel_layer.group_discard)(
                self.admin_room, self.channel_name
            )

        print(f"User {self.user} disconnected")

    def receive(self, text_data):
        data = json.loads(text_data)

        # Either conversation_id or receiver_id must be provided
        conversation_id = data.get("conversation_id")
        receiver_id = data.get("receiver_id")  # For new conversations
        message_text = data.get("message")
        is_to_admin = data.get("to_admin", False)

        conversation = None

        try:
            # Check if conversation_id is provided
            if conversation_id:
                # Check for existing user_to_user conversation in both directions
                receiver = User.objects.get(id=receiver_id)
                conversation = Conversation.objects.filter(id=conversation_id).first()

            # Otherwise, create or find conversation
            else:
                receiver = User.objects.get(id=receiver_id)

                if is_to_admin:
                    conversation = (
                        Conversation.objects.filter(conversation_type="user_to_user")
                        .filter(
                            Q(user=self.user, other_user=receiver)
                            | Q(user=receiver, other_user=self.user)
                        )
                        .first()
                    )

                    # Create if not exists
                    if not conversation:
                        conversation = Conversation.objects.create(
                            user=self.user,
                            other_user=receiver,
                            conversation_type="user_to_user",
                        )
                else:
                    conversation = (
                        Conversation.objects.filter(conversation_type="user_to_user")
                        .filter(
                            Q(user=self.user, other_user=receiver)
                            | Q(user=receiver, other_user=self.user)
                        )
                        .first()
                    )

                    # Create if not exists
                    if not conversation:
                        conversation = Conversation.objects.create(
                            user=self.user,
                            other_user=receiver,
                            conversation_type="user_to_user",
                        )

            # Permission check
            if not conversation.can_user_access(self.user):
                self.send(json.dumps({"error": "Access denied."}))
                return

            # Save message
            message = Message.objects.create(
                conversation=conversation,
                sender=self.user,
                content=message_text,
            )

            response = {
                "conversation_id": conversation.id,
                "sender": self.user.full_name,
                "sender_id": self.user.id,
                "message": message_text,
                "timestamp": str(message.created_at),
            }

            group_name = f"conversation_{conversation.id}"

            # Add sender to group if not already added
            async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)

            # Send message to group
            async_to_sync(self.channel_layer.group_send)(
                group_name,
                {
                    "type": "chat_message",
                    "response": response,
                },
            )

        except User.DoesNotExist:
            self.send(json.dumps({"error": "Receiver user not found."}))
        except Conversation.DoesNotExist:
            self.send(json.dumps({"error": "Conversation not found."}))

    # Receive message from room group
    def chat_message(self, event):
        response = event["response"]

        # Send the message to WebSocket
        self.send(text_data=json.dumps(response))
