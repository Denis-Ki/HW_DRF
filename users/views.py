from rest_framework import viewsets, permissions
from rest_framework.generics import CreateAPIView

from users.models import Payment, User
from users.serializers import PaymentSerializer, UserSerializer

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filters_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['payment_date']


# class UserCreateAPIView(CreateAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     permission_classes = (permissions.AllowAny,)
#
#     def perform_create(self, serializer):
#         user = serializer.save(is_active=True)
#         user.set_password(user.password)
#         user.save()

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
