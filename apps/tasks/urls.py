from django.urls import path
from apps.tasks.views.tag_views import (
    TagListAPIView,
    TagDetailApiView
)
from apps.tasks.views.task_view import (
    AllTasksListAPIView,
    TaskDetailAPIView
)

urlpatterns = [
    path('', AllTasksListAPIView.as_view()),
    path('<int:pk>/', TaskDetailAPIView.as_view()),
    path('tags/', TagListAPIView.as_view()),
    path('tags/<int:tag_id>', TagDetailApiView.as_view()),
]

