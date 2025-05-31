from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from utils.services import send_custom_email

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
        status_new = Status.objects.get(name="New")
        data = request.data.copy()
        data["status"] = status_new.id
        serializer = CreateFeedbackSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            response = {
                "message": "Feedback created successfully.",
                "status": "success",
                "results": serializer.data,
            }
            if data.get("want_to_be_contacted"):
                subject = f"Feedback Received: {data.get('subject', 'No Subject')}"
                message = f"Thank you for your feedback, {data.get('name', 'User')}! We will get back to you soon."
                send_custom_email(
                    subject=subject,
                    message=message,
                    recipient_list=[data.get("email")],
                )

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
            "status": "success",
            "results": serializer.data,
        }
        return Response(response, status=status.HTTP_200_OK)
