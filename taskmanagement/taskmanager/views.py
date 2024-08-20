from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.core.cache import cache
from django.db.models import Q

# Create your views here.

User = get_user_model()


class TaskCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cache_key = f'task_list_{request.user.email}'
        task_list = cache.get(cache_key)
        if task_list is None:
            tasks = Task.objects.filter(user=request.user)
            if not tasks:
                return Response({'message':'Тасок нету'})
            serializer = TaskSerializer(tasks, many=True)
            task_list = serializer.data
            cache.set(cache_key, task_list, 300)
        return Response(task_list)

class TaskUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id, user=request.user)
        except Task.DoesNotExist:
            return Response({'message': 'Таска не найдена'}, status=status.HTTP_404_NOT_FOUND)

        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id, user=request.user)
        except Task.DoesNotExist:
            return Response({'message': 'Таска не найдена'}, status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response({'message': 'Таска успешно удалена'}, status=status.HTTP_204_NO_CONTENT)

class TaskSearchAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        query = request.query_params.get('query', '')
        if not query:
            return Response({'message': 'Пустой запрос'}, status=status.HTTP_400_BAD_REQUEST)
        if query:
            tasks = Task.objects.filter(Q(title__icontains=query) | Q(description__icontains=query), user=request.user)
            if tasks.exists():
                serializer = TaskSerializer(tasks, many=True)
                return Response(serializer.data)
            return Response({'message': 'Ничего не было найдено'}, status=status.HTTP_404_NOT_FOUND)