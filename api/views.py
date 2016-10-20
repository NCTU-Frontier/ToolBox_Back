from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics, viewsets, status
from .serializers import *
from django.conf import settings
import requests
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
from datetime import datetime

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
User = get_user_model()
NCTU_OAUTH_URL = 'https://id.nctu.edu.tw'


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	lookup_field = 'pk'


class NCTUSignUp(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = NCTUSignUpSerializer

	def create(self, request, *args, **kwargs):
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		code = serializer.data['code']
		get_token_url = NCTU_OAUTH_URL + '/o/token/'
		data = {
			'grant_type': 'authorization_code',
			'code': code,
			'client_id': settings.NCTU_CLIENT_ID,
			'client_secret': settings.NCTU_CLIENT_SECRET,
			'redirect_uri': settings.NCTU_REDIRECT_URI
		}
		# print(data)
		access_token = requests.post(get_token_url, data=data).json().get('access_token', None)
		# print(access_token)
		if access_token:
			headers = {
				'Authorization': 'Bearer ' + access_token
			}
			get_profile_url = NCTU_OAUTH_URL + '/api/profile/'
			data = requests.get(get_profile_url, headers=headers).json()
			email = data['d2_email']
			student_id = data['username']
			print(email, student_id)
			try:
				user = User.objects.get(email=email)
			except Exception as e:
				user = User(email=email, student_id=student_id)
				user.save()
			payload = jwt_payload_handler(user)
			print(payload)
			response = Response()
			response['token'] = jwt_encode_handler(payload)
			t = jwt_decode_handler(response['token'])
			print(t)
			return response
		else:
			# raise ValueError('Please Authorize Again')
			return Response('Please Authorize Again', status=status.HTTP_401_UNAUTHORIZED)
