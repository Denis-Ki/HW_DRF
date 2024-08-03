from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from cours.models import Lesson, Course, Subscription
from users.models import User
from django.urls import reverse

from django.contrib.auth import get_user_model

User = get_user_model()


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='user1@mail.com', password='pass1')
        self.course = Course.objects.create(title='Test_Course1')
        self.lesson = Lesson.objects.create(title='Lesson 1', description='Test lesson1',
                                            link_to_video='https://www.youtube.com/',
                                            course=self.course, owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_retrieve(self):
        url = reverse("cours:lesson_retrieve",
                      args=(self.lesson.pk,)
                      )
        response = self.client.get(url)
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), self.lesson.title
        )

    def test_lesson_create(self):
        url = reverse("cours:lesson_create")
        data = {
            'title': 'Lesson 1',
            'description': 'Test lesson1',
            'link_to_video': 'https://www.youtube.com/',
            "course": self.course.pk, "owner": self.user.pk
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED
        )
        self.assertEqual(
            Lesson.objects.all().count(), 2
        )

    def test_lesson_update(self):
        url = reverse("cours:lesson_update",
                      args=(self.lesson.pk,)
                      )
        data = {
            'title': 'Updated Lesson 1',
            'link_to_video': 'https://www.youtube.com/'
        }
        response = self.client.patch(url, data, format='json')
        data = response.json()
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        self.assertEqual(
            data.get("title"), 'Updated Lesson 1'
        )

    def test_lesson_delete(self):
        url = reverse("cours:lesson_destroy",
                      args=(self.lesson.pk,)
                      )
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code, status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Lesson.objects.all().count(), 0
        )

    def test_lesson_list(self):
        url = reverse("cours:lesson_list")
        response = self.client.get(url)
        self.assertEqual(
            response.status_code, status.HTTP_200_OK
        )
        result = {
            'count': Lesson.objects.all().count(),
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': lesson.pk,
                    'title': lesson.title,
                    'description': lesson.description,
                    'link_to_video': lesson.link_to_video,
                    'course': lesson.course.pk,
                    'owner': lesson.owner.pk,
                    "preview": None,
                } for lesson in Lesson.objects.all()
            ]
        }
        self.assertEqual(
            response.json(), result
        )

class SubscriptionAPITestCase(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create(email='user1@mail.com', password='pass1')
        self.course = Course.objects.create(title='Test Course')
        self.client.force_authenticate(user=self.user)
        self.subscription_data = {
            'course_id': self.course.id
        }

    def test_create_subscription(self):
        url = reverse('cours:subscription_create')
        data = self.subscription_data
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Подписка добавлена')
        self.assertTrue(Subscription.objects.filter(sab_user=self.user, sab_course=self.course).exists())
