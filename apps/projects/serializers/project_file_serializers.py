from rest_framework import serializers

from apps.projects.models import ProjectFile
from apps.projects.utils.upload_file_helper import (
    validate_file_extension,
    create_file_path,
    validate_file_size,
    save_file
)


class AllProjectFileSerializer(serializers.ModelSerializer):

    project = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
        many=True
    )

    class Meta:
        model = ProjectFile
        fields = [
            "id",
            "file_name",
            "project"
        ]


class CreateProjectFileSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectFile
        fields = ["file_name"]

    def validate_file_name(self, value):
        # file_name = value.split(".")[0] TODO: ACSII
        if not value.isascii():
            raise serializers.ValidationError(
                "File name is not ASCII"
            )
        if not validate_file_extension(value):
            raise serializers.ValidationError(
                "File extension should be one of this type: .pdf, .csv, .doc, .xlsx"
            )
        return value

    def create(self, validated_data):
        project = self.context.get("project", None)
        file = self.context.get("file", None)

        file_path = create_file_path(
            file_name=validated_data.get("file_name"),
            project_name=project.name
        )
        if not validate_file_size(file):
            raise serializers.ValidationError(
                "File should be less than 2 Mb."
            )
        save_file(file, file_path)
        validated_data["file_path"] = file_path
        project_file = ProjectFile.objects.create(**validated_data)
        project_file.project.add(project)
        return project_file
