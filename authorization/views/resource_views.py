from rest_framework import viewsets, permissions
from ..models import User, Institution
from ..serializer import InstitutionSerializer, UserSerializer

class InstitutionViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD of institutions"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for CRUD of users"""
    permission_classes = [permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer