from rest_framework import viewsets

from users.models import Payment
from users.serializers import PaymentSerializer


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filters_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['payment_date']

