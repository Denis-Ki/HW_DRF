from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from users.apps import UsersConfig
from users.views import PaymentViewSet, UserViewSet
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


app_name = UsersConfig.name
router = DefaultRouter()

router.register(r'', UserViewSet, basename='users')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(permission_classes=(AllowAny,)), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(permission_classes=(AllowAny,)), name="token_refresh"),
    path('', include(router.urls)),
]
