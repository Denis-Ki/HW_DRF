from cours.models import Course, Lesson
from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name="Email адрес")

    phone = PhoneNumberField(
        verbose_name="телефон",
        **NULLABLE,
        help_text="Введите номер телефона",
    )
    city = models.CharField(
        max_length=50,
        verbose_name="город",
        **NULLABLE,
        help_text="Введите город",
    )
    avatar = models.ImageField(
        upload_to="users/avatars/",
        verbose_name="аватар",
        **NULLABLE,
        help_text="Загрузите аватар",
    )

    token = models.CharField(
        max_length=100, verbose_name="Token", **NULLABLE
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email


class Payment(models.Model):
    PAYMENT_METHODS = (("cash", "Наличные"), ("transfer", "Перевод на счёт"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments", **NULLABLE
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="payments", blank=True, null=True
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="payments", blank=True, null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    session_id = models.CharField(max_length=255, **NULLABLE, verbose_name="Session ID")
    link = models.URLField(max_length=400, verbose_name="ссылка на платеж", **NULLABLE)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Payment of {self.amount} by {self.user}"



