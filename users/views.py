from rest_framework import viewsets, permissions, generics
from rest_framework.generics import CreateAPIView

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from users.services import create_stripe_price, crate_stripe_session


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filters_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['payment_date']


class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        price = create_stripe_price(payment.amount)
        session_id, payment_link = crate_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = (permissions.AllowAny,)
        else:
            self.permission_classes = (permissions.IsAuthenticated,)
        return super().get_permissions()

    def perform_create(self, serializer):
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def perform_update(self, serializer):
        user = serializer.save()
        if 'password' in self.request.data:
            user.set_password(self.request.data['password'])
            user.save()

    def perform_destroy(self, instance):
        instance.delete()
