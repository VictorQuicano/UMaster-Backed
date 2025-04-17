# services/token_service.py
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
from rest_framework_simplejwt.exceptions import TokenError
import jwt
from django.conf import settings


class TokenService:
    """Service specialized in generating and managing JWT tokens"""

    @staticmethod
    def generate_token_for_user(user):
        """Generates a JWT token for a user"""
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    @staticmethod
    def blacklist_token(refresh_token):
        """Add a token to the blacklist, invalidating it"""
        token = RefreshToken(refresh_token)
        token.blacklist()

    @staticmethod
    def blacklist_all_user_tokens(user):
        """Invalidates all tokens for a user"""
        for token in OutstandingToken.objects.filter(user=user):
            try:
                refresh_token = RefreshToken(token.token)
                refresh_token.blacklist()
            except TokenError:
                pass  # Token ya inválido o en lista negra

    @staticmethod
    def decode_token(token):
        """Decodes a JWT token"""
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

    @staticmethod
    def refresh_access_token(refresh_token):
        """Creates a new access token using a refresh token"""
        refresh = RefreshToken(refresh_token)
        return str(refresh.access_token)
