from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def validated_data(self, attrs):
        email = attrs.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            return attrs
        raise serializers.ValidationError("Этот пользователь уже зарегистрирован")

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user