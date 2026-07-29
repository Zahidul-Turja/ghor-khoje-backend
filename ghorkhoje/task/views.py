import traceback
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from task.models import Task, TaskCategory, TaskPriority

from utils.responses import common_response
from task.serializers import TaskCreationSerializer, TaskSerializer


# Create your views here.
class TaskCreationAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            data = request.data.copy()
            data["user"] = request.user.id
            serializer = TaskCreationSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return_data = TaskSerializer(
                serializer.instance, context={"request": request}
            )
            return common_response(
                200, "Task created successfully.", data=return_data.data
            )
        except Exception as e:
            traceback.print_exc()
            return common_response(400, str(e))


class TaskUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.filter(id=pk).first()
            if not task:
                return common_response(404, "Task not found.")

            if task.user != request.user:
                return common_response(
                    403, "You are not authorized to update this task."
                )

            serializer = TaskSerializer(task, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = TaskSerializer(task, context={"request": request}).data
            return common_response(200, "Task updated successfully.", data=data)
        except Exception as e:
            traceback.print_exc()
            return common_response(400, str(e))


class TaskDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            task = Task.objects.filter(id=pk).first()
            if not task:
                return common_response(404, "Task not found.")

            if task.user != request.user:
                return common_response(
                    403, "You are not authorized to delete this task."
                )

            task.delete()
            return common_response(200, "Task deleted successfully.")
        except Exception as e:
            return common_response(400, str(e))


class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            tasks = Task.objects.filter(user=request.user).order_by("-created_at")
            serializer = TaskSerializer(tasks, many=True, context={"request": request})
            return common_response(200, "Tasks fetched successfully.", serializer.data)
        except Exception as e:
            return common_response(400, str(e))


class TaskToggleCompletedAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        try:
            task = Task.objects.filter(id=pk).first()
            if not task:
                return common_response(404, "Task not found.")

            if task.user != request.user:
                return common_response(
                    403, "You are not authorized to update this task."
                )

            task.is_complete = not task.is_complete
            task.save()

            return common_response(200, "Task status updated successfully.")
        except Exception as e:
            return common_response(400, str(e))
