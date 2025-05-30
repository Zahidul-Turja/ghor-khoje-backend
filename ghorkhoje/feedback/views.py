from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from feedback.models import *
from feedback.serializers import *


# Create your views here.
class FeedbackTypeListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        feedback_types = FeedbackType.objects.all()
        serializer = FeedbackTypeSerializer(feedback_types, many=True)
        response = {
            "message": "Feedback types retrieved successfully.",
            "status": status.HTTP_200_OK,
            "results": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


class StatusListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        statuses = Status.objects.all()
        serializer = StatusSerializer(statuses, many=True)
        response = {
            "message": "Status list retrieved successfully.",
            "status": status.HTTP_200_OK,
            "results": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)


class CreateFeedbackView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = CreateFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Feedback created successfully.",
                "status": status.HTTP_201_CREATED,
                "results": serializer.data,
            }
            # Optionally, you can send an email notification here
            # send_email_notification(serializer.data)

            return Response(response, status=status.HTTP_201_CREATED)
        response = {
            "message": "Failed to create feedback.",
            "status": status.HTTP_400_BAD_REQUEST,
            "errors": serializer.errors,
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class FeedbackListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        feedbacks = Feedback.objects.all()
        serializer = FeedbackSerializer(feedbacks, many=True)
        response = {
            "message": "Feedbacks retrieved successfully.",
            "status": status.HTTP_200_OK,
            "results": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
