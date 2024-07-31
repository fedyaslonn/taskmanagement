from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = (
        ('new', 'Новая'),
        ('in_progress', 'В процессе'),
        ('completed', 'Завершена'),
    )
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title