from rest_framework import serializers
from apps.projects.models import Project


class AllProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ('id', 'name', 'created_at')


class CreateUpdateProjectSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Project
        fields = ('name', 'description', 'created_at')

    def validate_description(self, value):
        if len(value) < 50:
            raise serializers.ValidationError('Description must be at least 50 characters')
        return value


class ProjectDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'description', 'created_at', 'count_of_files']


class ProjectShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['name', 'created_at']
