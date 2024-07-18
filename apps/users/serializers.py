import re
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from rest_framework import serializers

from apps.users.models import User


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "position",
            "email",
            "phone",
            "last_login"
        ]

class RegisterUserSerializer(serializers.ModelSerializer):

    re_password = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "position",
            "password",
            "re_password"
        ]
        extra_kwargs = {"password": {
            "write_only": True
        }}

    def validate(self, attrs):
        user_name = attrs.get('username')
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')

        if not re.match('^[A-Za-z0-9_.]+$', user_name):
            raise serializers.ValidationError(
                {'user_name': 'The username must be alphanumeric characters or have only _ . symbols.'}
            )
        if not re.match('^[A-Za-z]+$', first_name):
            raise serializers.ValidationError(
                {'first_name': 'The first_name must be alphabet characters.'}
            )
        if not re.match('^[A-Za-z]+$', last_name):
            raise serializers.ValidationError(
                {'last_name': 'The last_name must be alphabet characters.'}
            )

        password = attrs.get('password')
        re_password = attrs.get('re_password')

        if password != re_password:
            raise serializers.ValidationError(
                {'password': 'Password must be same.'}
            )

        try:
            validate_password(password)
        except ValidationError as err:
            raise serializers.ValidationError(
                {'password': err.messages}
            )
        return attrs

    def create(self, validated_data):
        password = validated_data.get('password')
        validated_data.pop('re_password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()

        return user
