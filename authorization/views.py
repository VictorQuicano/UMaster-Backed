from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.db.models import Q
from django.urls import reverse
from umaster.utils import Util
import jwt
from jwt.exceptions import ExpiredSignatureError
from rest_framework_simplejwt.tokens import RefreshToken

from datetime import datetime, timedelta

from .serializer import RegisterSerializer, InstitutionSerializer, EmailVerificationSerializer, UserSerializer, \
    LoginSerializer
from .models import User, Institution

class InstitutionView(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
  
class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class MailableWithToken(APIView):
    permission_classes = [permissions.AllowAny]

    def send_mail_with_token(self, user:User, request):
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = 'http://' + current_site + relativeLink + "?token=" + str(token)
        email_body = 'Hi ' + user.username + \
                     ' Use the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email': user.email,
                'email_subject': 'Verify your email'}

        Util.send_email(data)

class RegisterView(MailableWithToken):

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.save()
            user = User.objects.get(email=user.email)
            self.send_mail_with_token(user, request)

            return Response({'message': 'Usuario creado. Verifica tu email.'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReSentVerificationEmail(MailableWithToken):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', None)
        if email is None:
            return Response({'error': 'Email not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({'message': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)

            self.send_mail_with_token(user, request)

            return Response({'message': 'Verification email sent'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class VerifyEmailView(APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            # Decode the token to get the user ID
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_active:
                user.is_active = True
                user.save()
            return Response({'email': 'Successfully activated'}, status=status.HTTP_200_OK)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
        except ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email', None)
        if email is None:
            return Response({'error': 'Email not provided'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response({'message': 'Email already verified'}, status=status.HTTP_400_BAD_REQUEST)

            self.send_mail_with_token(user, request)

            return Response({'message': 'Verification email sent'}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email_username = serializer.validated_data['email_username']
        password = serializer.validated_data['password']

        try:
            user = User.objects.get(Q(email=email_username) | Q(username=email_username))
        except User.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_active:
            return Response({'error': 'Email not verified'}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_200_OK)