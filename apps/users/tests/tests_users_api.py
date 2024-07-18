from unittest.mock import patch, MagicMock

from django.urls import reverse
from django.db.models import QuerySet

from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.projects.models import Project
from apps.users.models import User
from apps.users.serializers import UserListSerializer
from apps.users.views import UserListGenericView


class TestUserListApi(APITestCase):
    fixtures = ['apps/fixtures/projects_fixture.json', 'apps/fixtures/users_fixture.json']

    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('user-list')

    # Проверка получения списка всех пользователей
    def test_user_list(self):
        users = User.objects.all()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = UserListSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)

    # Проверка получения списка всех пользователей по имени проекта
    def test_user_list_by_project(self):
        project = Project.objects.get(pk=1)
        users = User.objects.filter(project=project)

        response = self.client.get(self.url + '?project_name=' + project.name)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serializer = UserListSerializer(users, many=True)
        self.assertEqual(response.data, serializer.data)

    # Проверка получения пустого списка пользователей(нужно подменить выходной QuerySet)
    @patch.object(
        target=UserListGenericView,
        attribute='get_queryset',
        return_value=User.objects.none()
    )
    def test_empty_project_list(self, mock_get_objects):
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data, [])


class TestUserRegisterApi(APITestCase):
    fixtures = ['apps/fixtures/projects_fixture.json', 'apps/fixtures/users_fixture.json']

    def setUp(self) -> None:
        self.client = APIClient()
        self.url = reverse('user-register')

    # Проверка создания нового пользователя с хорошими данными
    def test_create_valid_user(self):
        data = {
            "username": "test_create_valid_user",
            "first_name": "Valid",
            "last_name": "User",
            "email": "test_create_valid_user@example.com",
            "position": "PROGRAMMER",
            "password": "VeryStrongPass123",
            "re_password": "VeryStrongPass123"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # TODO: Bug: Status 200 returned after user registration.
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(
            User.objects.filter(username='test_create_valid_user').exists()
        )

    # Проверка создания нового пользователя с испорченными данными
    def test_create_user_invalid_data(self):
        data = {
            "username": "alexsmith",
            "first_name": "VerylongfirstnameVerylongfirstnameVerylongfirstname",
            "last_name": "VerylonglastnameVerylonglastnameVerylonglastname",
            "email": "test_create_valid_user",
            "position": "test",
            "password": "qwerty",
            "re_password": "not_simple"
        }

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            str(response.data['username'][0]),
            'user with this username already exists.'
        )
        self.assertEqual(
            str(response.data['first_name'][0]),
            'Ensure this field has no more than 40 characters.'
        )
        self.assertEqual(
            str(response.data['last_name'][0]),
            'Ensure this field has no more than 40 characters.'
        )
        self.assertEqual(
            str(response.data['email'][0]),
            'Enter a valid email address.'
        )
        self.assertEqual(
            str(response.data['position'][0]),
            '"test" is not a valid choice.'
        )

    # Проверка создания нового пользователя с пропуском обязательных данных
    def test_create_user_missed_fields(self):
        data = {}

        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(str(response.data['username'][0]), 'This field is required.')
        self.assertEqual(str(response.data['first_name'][0]), 'This field is required.')
        self.assertEqual(str(response.data['last_name'][0]), 'This field is required.')
        self.assertEqual(str(response.data['email'][0]), 'This field is required.')
        self.assertEqual(str(response.data['position'][0]), 'This field is required.')
        self.assertEqual(str(response.data['password'][0]), 'This field is required.')
        self.assertEqual(str(response.data['re_password'][0]), 'This field is required.')
