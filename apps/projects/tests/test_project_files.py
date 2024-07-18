from django.db.models import QuerySet
from django.test import TestCase
from unittest.mock import patch, Mock, MagicMock
from rest_framework import status

from apps.projects.models import ProjectFile, Project
from apps.projects.serializers.project_file_serializers import CreateProjectFileSerializer


class ProjectFileListGenericViewTest(TestCase):
    field_types = {
        'id': int,
        'file_name': str,
        'project': list
    }

    exp_values = {
        'id': 1,
        'file_name': 'test_file.txt',
        'project': ['Test Project'],
    }

    @patch('apps.projects.views.project_files_views.ProjectFileListGenericView.get_queryset')
    def test_get_empty_project_files(self, mock_get_queryset):
        # Создаем mock объект QuerySet
        mock_empty_queryset = Mock(spec=QuerySet)
        mock_empty_queryset.exists.return_value = False
        mock_empty_queryset.return_value = iter([])

        mock_get_queryset.return_value = mock_empty_queryset

        response = self.client.get('/api/v1/projects/files/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.data, list)
        self.assertEqual(len(response.data), 0)

        mock_get_queryset.assert_called_once()

    @patch('apps.projects.views.project_files_views.ProjectFileListGenericView.get_queryset')
    def test_get_project_files_with_project_name(self, mock_get_queryset):
        project = Project.objects.create(
            name='Test Project',
            description='Test Project name for test cases with mock data.'
        )

        # Создаем фейковые данные для возвращаемого значения
        proj_file = ProjectFile.objects.create(
            file_name='test_file.txt',
            file_path='test/file/path/test_file.txt',
        )

        project.files.add(proj_file)

        mock_queryset = MagicMock(spec=QuerySet)
        mock_queryset.exists.return_value = True
        mock_queryset.__iter__.return_value = iter([proj_file])

        mock_get_queryset.return_value = mock_queryset

        response = self.client.get('/api/v1/projects/files/?project_name=Test%20Project')
        response_data = response.data[0]

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

        for attr, expected_type in self.field_types.items():
            with self.subTest(attr=attr, expected_type=expected_type):
                self.assertIsInstance(response_data.get(attr), expected_type)

        for attr, expected_value in self.exp_values.items():
            with self.subTest(attr=attr, expected_value=expected_value):
                if isinstance(expected_value, dict):
                    for key, value in expected_value.items():
                        self.assertEqual(response_data.get(attr, {}), value)
                else:
                    self.assertEqual(response_data.get(attr), expected_value)

        mock_get_queryset.assert_called_once()


class TestCreateProjectFileSerializer(TestCase):
    @patch('apps.projects.serializers.project_file_serializers.save_file')
    def test_create_project_file(self, mock_save_file):
        mock_save_file.return_value = 'documents/Mock_Project/mock_file.pdf'

        project = Project.objects.create(
            name='Mock Project',
            description='Mock Project description with length minimum of 50 characters'
        )

        mock_file = Mock()
        mock_file.name = 'mock_file.pdf'
        mock_file.size = 1024 * 1024  # 1 MB

        context = {
            "project": project,
            "file": mock_file
        }

        data = {
            "file_name": "mock_file.pdf"
        }

        serializer = CreateProjectFileSerializer(
            data=data,
            context=context
        )

        self.assertTrue(serializer.is_valid(), serializer.errors)

        project_file = serializer.save()

        mock_save_file.assert_called_once_with(
            mock_file,
            'documents/Mock_Project/mock_file.pdf'
        )

        self.assertEqual(
            project_file.file_path,
            'documents/Mock_Project/mock_file.pdf'
        )

        self.assertEqual(project_file.file_name, 'mock_file.pdf')
        self.assertEqual(project_file.project.first(), project)

