from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response

from apps.users.models import User
from apps.users.serializers import UserListSerializer, RegisterUserSerializer


class UserListGenericView(ListAPIView):

    serializer_class = UserListSerializer

    def get_queryset(self):
        project_name = self.request.query_params.get("project_name")
        if project_name:
            return User.objects.filter(
                project__name=project_name
            )
        return User.objects.all()

    def list(self, request: Request, *args, **kwargs) -> Response:
        query_set = self.get_queryset()
        if query_set.exists():
            serializer = self.get_serializer(query_set, many=True)
            return Response(
                data=serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )


class RegisterUserGenericView(CreateAPIView):
    serializer_class = RegisterUserSerializer

    def create(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )
