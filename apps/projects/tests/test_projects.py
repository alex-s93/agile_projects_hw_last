from unittest.mock import patch, MagicMock

from django.urls import reverse
from django.db.models import QuerySet

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.projects.models import Project
from apps.projects.serializers.project_serializers import (
    AllProjectsSerializer, ProjectDetailSerializer
)
from apps.projects.views.project_views import ProjectListAPIView, ProjectDetailAPIView


class TestProjectListAPIView(APITestCase):

    def setUp(self) -> None:
        self.client = APIClient()  # по умолчанию анонимный юзер
        self.url = reverse('project-list')

        self.project1 = Project.objects.create(
            name='Project 1',
            description='Mock Project description with length minimum of 50 characters'
        )
        self.project2 = Project.objects.create(
            name='Project 2',
            description='Mock Project description with length minimum of 50 characters'
        )

    @patch.object(
        target=ProjectListAPIView,
        attribute='get_objects',
        return_value=Project.objects.none()
    )
    def test_empty_project_list(self, mock_get_objects):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data, [])

    @patch.object(ProjectListAPIView, 'get_objects')
    def test_get_project_list(self, mock_get_objects):
        projects = [self.project1, self.project2]

        mock_queryset = MagicMock(spec=QuerySet)
        mock_queryset.__iter__.return_value = iter(projects)
        mock_get_objects.return_value = mock_queryset

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка содержимого ответа
        serializer = AllProjectsSerializer(projects, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_create_project(self):
        data = {
            'name': 'New Project',
            'description': 'Test Description for the first test project with description more than 50 chars.'
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверка данных созданного проекта
        self.assertTrue(Project.objects.filter(name='New Project').exists())
        project = Project.objects.get(name='New Project')
        self.assertEqual(
            project.description,
            'Test Description for the first test project with description more than 50 chars.'
        )


class TestRetrieveUpdateProjectAPIView(APITestCase):
    fixtures = ['apps/fixtures/projects_fixture.json']

    def setUp(self):
        self.client = APIClient()
        self.mock_project = Project.objects.create(
            name='Test Project',
            description='Description for test project'
        )
        self.project = Project.objects.get(pk=1)
        self.url = reverse('project-detail', kwargs={'pk': 1})

    @patch.object(ProjectDetailAPIView, 'get_object')
    def test_update_project(self, mock_get_object):
        mock_get_object.return_value = self.mock_project
        data = {
            'name': 'Updated Project',
        }

        response = self.client.put(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверка данных обновленного проекта
        self.mock_project.refresh_from_db()
        self.assertEqual(self.mock_project.name, 'Updated Project')

    def test_delete_project(self):
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'message': 'Project deleted successfully'})

        # Проверка, что проект был удален из базы данных
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_get_project(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = ProjectDetailSerializer(self.project)
        self.assertEqual(response.data, serializer.data)
