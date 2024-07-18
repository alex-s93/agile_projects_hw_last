from django.test import TestCase
from unittest.mock import MagicMock
from rest_framework.response import Response
from rest_framework import status


class TestProjectResponseClass(TestCase):
    def test_response_object(self):
        mock_response = MagicMock(spec=Response)

        mock_response.status_code = 200
        mock_response.data = {'key': 'value'}
        mock_response.__str__.return_value = '200 OKEY'

        self.assertEqual(mock_response.status_code, status.HTTP_200_OK)
        self.assertEqual(mock_response.data, {'key': 'value'})
        self.assertEqual(str(mock_response), '200 OKEY')
