from django.db import models


NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name="название")
    preview = models.ImageField(upload_to="blog", verbose_name="изображение", **NULLABLE)
    description = models.TextField(verbose_name="описание", **NULLABLE)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name="course_owner", **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    preview = models.ImageField(upload_to="blog", verbose_name="изображение", **NULLABLE)
    link_to_video = models.TextField(verbose_name="ссылка на видео", **NULLABLE)
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, verbose_name="курс",
    )
    owner = models.ForeignKey(
        'users.User', on_delete=models.CASCADE, related_name="lesson_owner", **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    sab_course = models.ForeignKey(Course, on_delete=models.CASCADE, **NULLABLE, verbose_name='подписка на курс')
    sab_user = models.ForeignKey('users.User', on_delete=models.CASCADE, **NULLABLE, verbose_name='кто подписан на курс')
    sab_activ = models.BooleanField(default=True, verbose_name='подписан не подписан')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.sab_user.email} подписан на {self.sab_course.title}'
