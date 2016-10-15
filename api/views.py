from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics, viewsets, status
from django.contrib.auth import get_user_model
from .serializers import *

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	lookup_field = 'username'
