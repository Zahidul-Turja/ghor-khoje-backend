from rest_framework import serializers
from user.models import Review
from user.serializers import UserProfileSerializer


class ReviewSerializer(serializers.ModelSerializer):
    reviewer = UserProfileSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "reviewer", "overall", "review_text", "created_at"]
