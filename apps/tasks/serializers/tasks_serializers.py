from rest_framework import serializers
from django.utils import timezone

from apps.tasks.models import Task, Tag
from apps.projects.models import Project
from apps.tasks.choices.priorities import Priorities
from apps.projects.serializers.project_serializers import ProjectShortInfoSerializer
from apps.users.models import User


class AllTasksSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        read_only=True,
        slug_field='name'
    )
    assignee = serializers.SlugRelatedField(
        read_only=True,
        slug_field='email'
    )

    class Meta:
        model = Task
        fields = ('name', 'status', 'priority', 'project', 'assignee', 'deadline')


class CreateUpdateTaskSerializer(serializers.ModelSerializer):
    project = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Project.objects.all()
    )
    assignee = serializers.SlugRelatedField(
        slug_field='email',
        queryset=User.objects.all(),
        required=False
    )

    class Meta:
        model = Task
        fields = ('name', 'description', 'priority', 'status', 'assignee', 'project', 'tags', 'deadline')

    def validate_name(self, value):
        if len(value) < 10:
            raise serializers.ValidationError('Name must be at least 10 characters')
        return value

    def validate_description(self, value):
        if len(value) < 50:
            raise serializers.ValidationError('Description must be at least 50 characters')
        return value

    def validate_priority(self, value):
        if value not in [item[0] for item in Priorities.choices()]:
            raise serializers.ValidationError(
                "The priority of the task couldn't be one of the available options"
            )
        return value

    def validate_project(self, value):
        if not Project.objects.filter(name=value).exists():
            raise serializers.ValidationError('Project not found')
        return value

    def validate_tags(self, value):
        if not Tag.objects.filter(name__in=value).exists():
            raise serializers.ValidationError('Tags not found')
        return value

    def validate_deadline(self, value):
        # value = timezone.make_aware(value, timezone.get_current_timezone())
        if value < timezone.now():
            raise serializers.ValidationError(
                'Deadline time can not be in past'
            )
        return value

    def create(self, validated_data):
        tags = validated_data.pop('tags', [])
        task = Task.objects.create(
            **validated_data
        )
        for tag in tags:
            task.tags.add(tag)
        task.save()
        return task

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', [])

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.tags.add(*tags)
        instance.save()
        return instance


class TaskDetailSerializer(serializers.ModelSerializer):
    project = ProjectShortInfoSerializer()

    class Meta:
        model = Task
        exclude = ('updated_at', 'deleted_at')
