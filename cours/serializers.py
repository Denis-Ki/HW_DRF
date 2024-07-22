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
