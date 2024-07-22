from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cours.views import CourseViewSet
from cours.views import LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView

from cours.apps import CoursConfig

app_name = CoursConfig.name


router = DefaultRouter()
router.register(r'', CourseViewSet, basename='course')


urlpatterns = [
    path('', include(router.urls)),
    path('lesson', LessonListAPIView.as_view(), name='lesson_list'),
    path('lesson/create', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lesson/update/<int:pk>', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/<int:pk>/destroy', LessonDestroyAPIView.as_view(), name='lesson_destroy'),
]
