from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *
from django.contrib.auth.password_validation import validate_password

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'bio', 'location', 'birth_date', 'username']
        extra_kwargs = {'password': {'write_only': True}}
        read_only_fields = ['id']

    def create(self, validated_data):
        user = User(
            email=validated_data.get('email'),
            username=validated_data.get('username', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

class ChangePasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_new_password(self, value):
        validate_password(value)
        return value