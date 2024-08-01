from celery.schedules import crontab
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from celery import Celery, shared_task
from celery.schedules import crontab
from datetime import datetime, timedelta

User = get_user_model()
@shared_task
def admin_notification():
    new_users_count = User.objects.filter(date_joined__gte=datetime.now()-timedelta(days=1)).count()
    subject = 'Отчет о новых пользователях'
    message = f'За последние 24 часа количество новых пользователей - {new_users_count}'
    from_email = settings.EMAIL_HOST_USER
    to_email = settings.EMAIL_HOST_USER
    send_mail(subject, message, from_email, [to_email])

