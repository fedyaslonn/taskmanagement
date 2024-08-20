from django.urls import path
from .views import (
    RegisterAPIView,
    LoginAPIView,
    ChangePassAPIView,
    UserAPIView,
    UserUpdateAPIView,
)

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('change_password/', ChangePassAPIView.as_view(), name='change_pass'),
    path('info/', UserAPIView.as_view(), name='user'),
    path('user/reset/', UserUpdateAPIView.as_view(), name='user_reset'),
]