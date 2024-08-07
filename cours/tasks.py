from datetime import timedelta, timezone
from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone
from cours.models import Subscription
from users.models import User


@shared_task
def notify_subscribers(course_id):
    """Рассылка пользователям на обновления контента курса"""
    subscriptions = Subscription.objects.filter(sab_course=course_id)
    for subscription in subscriptions:
        user = subscription.sab_user

        send_mail(
            'Новый курс на платформе',
            f'На платформе обновился курс: {subscription.sab_course.title}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email],
            fail_silently=False,
        )


@shared_task
def check_last_login():
    """Переодическая задача для проверки не активных пользователей """

    inactive_period = timedelta(days=30)
    threshold_date = timezone.now() - inactive_period
    inactive_users = User.objects.filter(last_login__lt=threshold_date)

    for user in inactive_users:
        if user.is_active:
            user.is_active = False
            user.save()
            print(f'Пользователь {user.email} не заходил более месяца, поэтому заблокирован')