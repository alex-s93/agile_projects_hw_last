from django.test import TestCase

from apps.users.models import User
from apps.users.serializers import UserListSerializer, RegisterUserSerializer


class TestUserSerializers(TestCase):
    fixtures = ['apps/fixtures/projects_fixture.json', 'apps/fixtures/users_fixture.json']

    # Проверка работы сериализатора на правильное отображение данных списка пользователей
    def test_user_list_serializer(self):
        user = User.objects.get(pk=3)
        serializer = UserListSerializer(user)
        self.assertEqual(serializer.data['first_name'], user.first_name)
        self.assertEqual(serializer.data['last_name'], user.last_name)
        self.assertEqual(serializer.data['email'], user.email)
        self.assertEqual(serializer.data['position'], user.position)
        self.assertEqual(serializer.data['phone'], user.phone)
        self.assertEqual(
            serializer.data['last_login'],
            user.last_login.isoformat(timespec='seconds').replace('+00:00', 'Z')
        )

    def test_user_register_serializer(self):
        data = {
            "username": "test_create_valid_user",
            "first_name": "Valid",
            "last_name": "User",
            "email": "test_create_valid_user@example.com",
            "position": "PROGRAMMER",
            "password": "VeryStrongPass123",
            "re_password": "VeryStrongPass123"
        }

        serializer = RegisterUserSerializer(data=data)
        self.assertTrue(serializer.is_valid())

