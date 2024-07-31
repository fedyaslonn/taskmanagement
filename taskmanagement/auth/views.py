from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from .celerytask import send_email

# Create your views here.


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            user = User.objects.filter(email=email).first()
            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Выполнен успешный вход',
                }, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Данные введены неверно'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Проверьте формат ввода данных'}, status=status.HTTP_400_BAD_REQUEST)

class ChangePassAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if not user or not user.check_password(serializer.validated_data['old_password']):
                return Response({'message': 'Неправильный ввод пароля'}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': 'Пароль успешно изменён'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = f'{request.user.id}'
        user_info = cache.get(cache_key)

        if user_info is None:
            serializer = UserSerializer(request.user)
            user_info = serializer.data
            cache.set(cache_key, user_info, 300)

        return Response(user_info)

class UserUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Данные успешно обновлены'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)