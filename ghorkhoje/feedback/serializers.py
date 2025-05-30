from rest_framework import serializers

from feedback.models import *


class FeedbackTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackType
        fields = "__all__"


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = "__all__"


class CreateFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    status = StatusSerializer()
    feedback_type = FeedbackTypeSerializer()

    class Meta:
        model = Feedback
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")
