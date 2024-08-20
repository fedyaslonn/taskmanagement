from django.urls import path
from .views import (
    TaskCreateAPIView,
    TaskListAPIView,
    TaskUpdateAPIView,
    TaskDeleteAPIView,
)

urlpatterns = [
    path('create/', TaskCreateAPIView.as_view(), name='task_create'),
    path('list/', TaskListAPIView.as_view(), name='task_list'),
    path('update/<int:task_id>/', TaskUpdateAPIView.as_view(), name='task_update'),
    path('delete/<int:task_id>/', TaskDeleteAPIView.as_view(), name='task_delete'),
]