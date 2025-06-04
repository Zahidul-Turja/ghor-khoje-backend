import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

# from chat_app.services import *


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        print("Connecting to chat consumer...")
        print("Scope:", self.scope)
        # if "user" in self.scope and "api_key" not in self.scope:
        #     # Company Support Agent (Admin)
        #     user = self.scope["user"]
        #     # agent = Agent.objects.filter(user=user).first()
        #     # self.room_name = f"admin_room_{agent.company.pk}"
        #     self.room_group_name = f"chat_{self.room_name}"

        # elif "company" in self.scope and "user_info" in self.scope:
        #     # Customer (Authenticated via API Key)
        #     company = self.scope["company"]
        #     user_info = self.scope["user_info"]

        #     # Create a room specific to this company's customer
        #     self.room_name = f"company_{company.pk}_user_{user_info['user_id']}"

        #     # Store user_info for later use
        #     self.customer_info = user_info

        # else:
        #     self.close()
        #     return

        # self.room_group_name = f"chat_{self.room_name}"

        # print("group name", self.room_group_name)
        # print(f"Connecting to room: {self.room_name}")

        # # Join the room group
        # async_to_sync(self.channel_layer.group_add)(
        #     self.room_group_name, self.channel_name
        # )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )
        print(f"{self.scope['user']} got disconnected.")

    # Receive message from WebSocket
    def receive(self, text_data):

        text_data_json = json.loads(text_data)
        text_data_json["is_agent"] = self.scope.get("is_agent", False)
        print("Scope:", self.scope)
        if text_data_json["is_agent"]:
            user = self.scope.get("user", None)
            # agent = Agent.objects.filter(user=user).first()
            # text_data_json["company_id"] = agent.company.pk
        else:
            text_data_json["company_id"] = self.scope.get("company", {}).pk
        print(text_data_json["is_agent"])
        if text_data_json["is_agent"]:
            text_data_json["agent"] = self.scope["user"]
            text_data_json["is_agent"] = True

        print(f"Received message: {text_data_json} from {self.scope['user']}")

        # Process the incoming message
        # data = create_message(**text_data_json)

        # data = ConversationMessageSerializer(data).data
        data = {}

        if text_data_json.get("is_agent", False):
            user_details = text_data_json.get("userdetails", None)
            user_details = self.scope.get("user_info", None)
            user_id = user_details.get("user_id", "")
            user_room_name = (
                f"chat_company_{text_data_json.get('company_id', '')}_user_{user_id}"
            )

            async_to_sync(self.channel_layer.group_send)(
                user_room_name,
                {"type": "chat_message", "response": data},
            )

            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "response": data},
            )
            print(f"Agent message sent to {user_room_name}")
            print(f"Admin message sent to group {self.room_group_name}")
        else:
            # Customer is sending a message
            async_to_sync(self.channel_layer.group_send)(
                self.room_group_name,
                {"type": "chat_message", "response": data},
            )

            # Ensure correct admin room name
            if "user" in self.scope:  # Check if agent is logged in
                admin_room_name = (
                    f"chat_admin_room_{text_data_json.get('company_id', '')}"
                )
            else:
                admin_room_name = (
                    f"chat_admin_room_{text_data_json.get('company_id', '')}"
                )
            print(f"Admin room name: {admin_room_name}")
            print(f"Customer message sent to {admin_room_name}")
            async_to_sync(self.channel_layer.group_send)(
                admin_room_name,
                {"type": "chat_message", "response": data},
            )

    # Receive message from room group
    def chat_message(self, event):
        response = event["response"]

        # Send the message to WebSocket
        self.send(text_data=json.dumps(response))
