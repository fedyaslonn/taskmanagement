from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from django.shortcuts import get_object_or_404

@shared_task
def send_email(user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    subject = 'С успешной регистрацией!'
    message = f'{user.username}, поздравляем Вас! Ваша регистрация прошла успешно.'
    from_email = settings.EMAIL_HOST_USER
    to_email = [user.email]
    send_mail(subject, message, from_email, to_email)
    print(f"Email успешно отправлена {user.email}")