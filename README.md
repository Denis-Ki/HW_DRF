
В соответствии с условиями заданий урока 24_1:

1) Создан новый Django-проект HW_DRF и подключены DRF в настройках проекта;
2) Созданы модели:
 2.1) Пользователь(User):
  - все поля от обычного пользователя, но авторизацию заменить на email;
  - телефон;
  - город;
  - аватарка.
 Модель пользователя размещена в приложении users
 2.2) Курс:
  - название,
  - превью (картинка),
  - описание.
 2.3) Урок:
  - название,
  - описание,
  - превью (картинка),
  - ссылка на видео.
 Модели курс и урок размещены в приложении cours
3) Описаны CRUD для моделей курса и урока. 
Для реализации CRUD для курса используованы Viewsets, а для урока - Generic-классы.
Для работы контроллеров описаны простейшие сериализаторы.