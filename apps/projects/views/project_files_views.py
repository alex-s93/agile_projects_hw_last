from django.http import FileResponse
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, get_object_or_404
from rest_framework.views import APIView

from apps.projects.models import Project, ProjectFile
from apps.projects.serializers.project_file_serializers import (
    CreateProjectFileSerializer,
    AllProjectFileSerializer
)


class ProjectFileListGenericView(ListCreateAPIView):
    def get_queryset(self):
        project_name = self.request.query_params.get("project_name")
        if project_name:
            return ProjectFile.objects.filter(
                project__name=project_name
            )
        return ProjectFile.objects.all()

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == 'GET':
            return AllProjectFileSerializer
        return CreateProjectFileSerializer

    def get(self, request: Request, *args, **kwargs)-> Response:
        project_files = self.get_queryset()
        if not project_files.exists():
            return Response(
                data=[],
                status=status.HTTP_204_NO_CONTENT
            )
        serializer = self.get_serializer(project_files, many=True)
        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request, *args, **kwargs) -> Response:
        file = request.FILES.get("file", None)
        project_id = request.data.get("project_id", None)
        request.data["file_name"] = file.name if file else None

        project = get_object_or_404(Project, pk=project_id)

        context = {
            "file": file,
            "project": project
        }

        serializer = self.get_serializer(data=request.data, context=context)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class ProjectFileDownloadApiView(APIView):
    def get(self, request: Request, *args, **kwargs) -> FileResponse | Response:
        project_object = get_object_or_404(ProjectFile, pk=self.kwargs.get("pk"))

        file = project_object.file_path.open()
        response = FileResponse(file, as_attachment=True)
        return response

