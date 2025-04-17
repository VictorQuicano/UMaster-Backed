from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.auth_views import RegisterView
from .views.auth_views import (
    RegisterView, ResendVerificationEmailView, VerifyEmailView,
    LoginView, LogoutView, RefreshTokenView,
    PasswordResetRequestView, ResetPasswordView
)
from .views.resource_views import InstitutionViewSet, UserViewSet

router = DefaultRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/', VerifyEmailView.as_view(), name='email-verify'),
    path('resend-verification/', ResendVerificationEmailView.as_view(), name='resend-verification'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', RefreshTokenView.as_view(), name='token-refresh'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
]