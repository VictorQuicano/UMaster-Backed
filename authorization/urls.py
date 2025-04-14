from django.urls import path, include
from rest_framework import routers
from authorization.views import RegisterView
from authorization.views import LoginView
from authorization.views import VerifyEmailView
from authorization.views import InstitutionView
from authorization.views import ReSentVerificationEmail
from authorization.views import UserView


urlpatterns = [
    path('users/', UserView.as_view({'get': 'list', 'post': 'create'}), name='user-list'),
    path('institutions/', InstitutionView.as_view({'get': 'list', 'post': 'create'}), name='institution-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('email-verify/', VerifyEmailView.as_view(), name='email-verify'),
    path('resent-verification-email/', ReSentVerificationEmail.as_view(), name='resent-verification-email'),
]