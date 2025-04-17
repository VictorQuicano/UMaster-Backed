# views/auth_views.py
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
from jwt.exceptions import ExpiredSignatureError, DecodeError

from ..models import User
from ..serializer import (
    RegisterSerializer,
    LoginSerializer,
    ResetPasswordSerializer
)
from umaster.services.email_service import EmailService
from umaster.services.token_service import TokenService


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        user.save()

        token = TokenService.generate_token_for_user(user).access_token
        EmailService.send_verification_email(user, token)

        return Response(
            {"message": "User created successfully!"},
            status=status.HTTP_201_CREATED,
        )


class ResendVerificationEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            if user.is_active:
                return Response(
                    {"message": "Email already verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = TokenService.generate_token_for_user(user).access_token
            EmailService.send_verification_email(user, token)

            return Response(
                {"message": "Verification email sent"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        token = request.GET.get("token")
        if not token:
            return Response(
                {"error": "Token not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            payload = TokenService.decode_token(token)
            user = User.objects.get(id=payload["user_id"])

            if not user.is_active:
                user.is_active = True
                user.save()

            return Response(
                {"email": "Successfully activated"},
                status=status.HTTP_200_OK
            )
        except DecodeError:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except ExpiredSignatureError:
            return Response(
                {"error": "Activation expired"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email_username = serializer.validated_data["email_username"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(
                Q(email=email_username) | Q(username=email_username)
            )

            if not user.check_password(password):
                raise User.DoesNotExist()

            if not user.is_active:
                return Response(
                    {"error": "Email not verified"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            tokens = TokenService.generate_token_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")
            if not refresh_token:
                return Response(
                    {"error": "Refresh token not provided"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            TokenService.blacklist_token(refresh_token)
            return Response(
                {"message": "Sesión cerrada"},
                status=status.HTTP_205_RESET_CONTENT
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class RefreshTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response(
                {"error": "Refresh token not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            access_token = TokenService.refresh_access_token(refresh_token)
            return Response(
                {"access": access_token},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get("email")
        if not email:
            return Response(
                {"error": "Email not provided"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(email=email)
            if not user.is_active:
                return Response(
                    {"message": "Email not verified"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            token = TokenService.generate_token_for_user(user).access_token
            EmailService.send_password_reset_email(user, token)

            return Response(
                {"message": "Password reset email sent"},
                status=status.HTTP_200_OK
            )
        except User.DoesNotExist:
            return Response(
                {"message": "If the email exists, a reset link has been sent"},
                status=status.HTTP_200_OK
            )


class ResetPasswordView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        token = validated_data["token"]
        password = validated_data["password"]

        try:
            payload = TokenService.decode_token(token)
            user = User.objects.get(id=payload["user_id"])

            if not user.is_active:
                return Response(
                    {"error": "Email not verified"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            TokenService.blacklist_all_user_tokens(user)

            user.set_password(password)
            user.save()

            tokens = TokenService.generate_token_for_user(user)

            return Response({
                "message": "Password reset successfully",
                **tokens
            }, status=status.HTTP_200_OK)

        except ExpiredSignatureError:
            return Response(
                {"error": "Token expired"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except DecodeError:
            return Response(
                {"error": "Invalid token"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )