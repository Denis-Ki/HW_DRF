from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from cours.models import Lesson, Course, Subscription
from cours.validators import LinkToVideoValidator


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkToVideoValidator(fields='link_to_video')]


class CourseDetailSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField(read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Course
        fields = ['title', 'description', "updated_at", 'lesson_count', 'lessons', "is_subscribed"]

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(course=obj).count()

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(sab_course=obj, sab_user=user, sab_activ=True).exists()


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'sab_course', 'sab_user', 'sab_activ']
