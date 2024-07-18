from django.urls import path

from apps.projects.views.project_files_views import ProjectFileListGenericView, ProjectFileDownloadApiView
from apps.projects.views.project_views import ProjectListAPIView, ProjectDetailAPIView


urlpatterns = [
    path('', ProjectListAPIView.as_view(), name='project-list'),
    path('<int:pk>/', ProjectDetailAPIView.as_view(), name='project-detail'),
    path('files/', ProjectFileListGenericView.as_view(), name='project-files'),
    path('files/download/<int:pk>', ProjectFileDownloadApiView.as_view(), name='download-file')
]
