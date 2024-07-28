from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from cours.models import Lesson, Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField(read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'description', 'lesson_count', 'lessons']

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()