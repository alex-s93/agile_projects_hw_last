from django.db import models

from apps.projects.models import Project
from apps.tasks.choices.priorities import Priorities
from apps.tasks.choices.statuses import Statuses
from apps.tasks.utils.set_date_time import calculate_end_of_month
from apps.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=120)
    description = models.TextField()
    status = models.CharField(max_length=15, choices=Statuses.choices(), default=Statuses.NEW)
    priority = models.SmallIntegerField(choices=Priorities.choices(), default=Priorities.MEDIUM[0])
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks")
    tags = models.ManyToManyField("Tag", related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(default=calculate_end_of_month)
    assignee = models.ForeignKey(User, on_delete=models.PROTECT, related_name="tasks", blank=True, null=True)

    def __str__(self):
        return f"Name: {self.name} | Status: {self.status}"

    class Meta:
        unique_together = ["name", "project"]
        ordering = ["-deadline"]
