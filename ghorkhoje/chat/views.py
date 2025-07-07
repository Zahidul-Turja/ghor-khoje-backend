from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q


from chat.serializers import *
from user.models import User


# Create your views here.
class AllConversationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        conversations = Conversation.objects.filter(
            Q(user=user) | Q(other_user=user)
        ).distinct()

        serializer = ConversationSerializer(
            conversations, many=True, context={"request": request}
        )
        return Response(
            {
                "status": "success",
                "message": "Conversations fetched successfully.",
                "data": serializer.data,
            }
        )


class AllMessagesAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, conversation_id):
        messages = Message.objects.filter(conversation=conversation_id)
        serializer = MessageSerializer(
            messages, many=True, context={"request": request}
        )
        return Response(
            {
                "status": "success",
                "message": "Messages fetched successfully.",
                "data": serializer.data,
            }
        )


class MessagesByUserIdAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        user = request.user
        other_user = User.objects.get(id=user_id)

        try:
            conversation = Conversation.objects.filter(
                Q(user=user, other_user=other_user)
                | Q(user=other_user, other_user=user)
            ).first()
            messages = Message.objects.filter(conversation=conversation)
            serializer = MessageSerializer(
                messages, many=True, context={"request": request}
            )
            return Response(
                {
                    "status": "success",
                    "message": "Messages fetched successfully.",
                    "data": serializer.data,
                }
            )
        except Conversation.DoesNotExist:
            return Response(
                {
                    "status": "failed",
                    "message": "Conversation not found.",
                }
            )
