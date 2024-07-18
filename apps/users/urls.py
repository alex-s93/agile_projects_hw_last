from django.urls import path

from apps.users.views import UserListGenericView, RegisterUserGenericView

urlpatterns = [
    path('', UserListGenericView.as_view(), name='user-list'),
    path('register/', RegisterUserGenericView.as_view(), name='user-register'),
]
