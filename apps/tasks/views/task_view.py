from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status

from rest_framework.generics import get_object_or_404

from apps.tasks.models import Task
from apps.tasks.serializers.tasks_serializers import (
    AllTasksSerializer,
    CreateUpdateTaskSerializer,
    TaskDetailSerializer
)


class TaskPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10


class AllTasksListAPIView(APIView):
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            self.permission_classes = [IsAuthenticated | IsAdminUser]

        return [permission() for permission in self.permission_classes]

    def get_objects(self):
        project_name = self.request.query_params.get('project')
        assignee_email = self.request.query_params.get('assignee')

        if project_name:
            return Task.objects.filter(project__name=project_name)
        elif assignee_email:
            return Task.objects.filter(assignee__email=assignee_email)
        else:
            return Task.objects.all()

    def get(self, request, *args, **kwargs):
        tasks = self.get_objects()

        if not tasks.exists():
            return Response(data=[], status=status.HTTP_204_NO_CONTENT)

        paginator = TaskPagination()
        paginated_tasks = paginator.paginate_queryset(tasks, request, view=self)

        if paginated_tasks is not None:
            serializer = AllTasksSerializer(paginated_tasks, many=True)

            return paginator.get_paginated_response(serializer.data)

        serializer = AllTasksSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print(self.request.user.is_anonymous)
        print(self.request.user.is_authenticated)
        print(self.request.user)
        serializer = CreateUpdateTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Sample post query
# {
#     "name": "Update endpoint to get all users"
#     "description": "Need add some validators, update route, add query params to filter users by project"
#     "priority": 4
#     "project": "NEW TIGER PROJECT"
#     "tags": ["Backend", "Frontend"]
#     "deadline": "2024-06-30"
# }

class TaskDetailAPIView(APIView):
    def get_object(self):
        return get_object_or_404(Task, pk=self.kwargs['pk'])

    def get(self, request: Request, *args, **kwargs):
        task = self.get_object()
        serializer = TaskDetailSerializer(task)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request: Request, *args, **kwargs):
        task = self.get_object()
        serializer = CreateUpdateTaskSerializer(instance=task, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request: Request, *args, **kwargs):
        task = self.get_object()

        task.delete()

        delete_message = {
            "message": "Task was successfully deleted"
        }
        return Response(data=delete_message, status=status.HTTP_200_OK)
