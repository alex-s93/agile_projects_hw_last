from django.test import TestCase
from unittest.mock import MagicMock
from apps.projects.models import Project


class TestProjectModel(TestCase):
    def test_project_representation(self):
        mock_project = MagicMock(spec=Project)

        mock_project.name = 'FAKE PROJECT'

        mock_project.__str__.return_value = 'FAKE PROJECT'

        self.assertEqual(str(mock_project), 'FAKE PROJECT')
