from django.shortcuts import render
from django.contrib.auth import get_user_model

from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.filters import SearchFilter

from .serializers import UserSerializer
from .permissions import UpdateSelfUserPermissions

# Create your views here.

class UserViewSet(ModelViewSet):
    """Handles User requests"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [UpdateSelfUserPermissions]
    authentication_classes = [TokenAuthentication]
    filter_backends = [SearchFilter]
    search_fields = ['id', 'email', 'name']


class UserLoginApiView(ObtainAuthToken):
    """Handles User Login"""

    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES