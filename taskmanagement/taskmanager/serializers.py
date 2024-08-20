from rest_framework import serializers
from .models import *

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'due_date', 'status']
        read_only_fields = ['id', 'created_at']