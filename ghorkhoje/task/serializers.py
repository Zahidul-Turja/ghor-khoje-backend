from rest_framework import serializers

from task.models import Task


class TaskCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            "user",
            "title",
            "description",
            "category",
            "priority",
            "due_date",
            "related_property",
        ]


class TaskSerializer(serializers.ModelSerializer):
    related_property = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "user",
            "title",
            "description",
            "category",
            "priority",
            "due_date",
            "related_property",
            "is_complete",
            "created_at",
        ]

    def get_related_property(self, obj):
        return PlaceTitleSerializer(obj.related_property, context=self.context).data


class BookmarksSerializer(serializers.Serializer):
    places = serializers.SerializerMethodField()

    def get_places(self, obj):
        return PlaceDetailsSerializer(
            obj.bookmarks, context=self.context, many=True
        ).data
