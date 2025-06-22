from rest_framework import serializers

from .models import Conversation, Message
from user.serializers import UserProfileSerializer


class ConversationSerializer(serializers.ModelSerializer):
    other_user = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "conversation_type",
            "other_user",
            "last_message",
            "other_user",
            "created_at",
        ]

    def get_other_user(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return None  # or raise an error or handle it as needed

        user = request.user
        other_person = obj.other_user if obj.other_user != user else obj.user
        return UserProfileSerializer(other_person, context={"request": request}).data

    def get_last_message(self, obj):
        if obj.messages.exists():
            return MessageSerializer(obj.messages.last(), context=self.context).data
        return ""


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SerializerMethodField()

    class Meta:
        model = Message
        fields = "__all__"

    def get_sender(self, obj):
        request = self.context.get("request", None)
        if request is None:
            return None  # or raise an error or handle it as needed

        return UserProfileSerializer(obj.sender, context={"request": request}).data
