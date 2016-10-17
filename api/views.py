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
		print(data)
		access_token = requests.post(get_token_url, data=data).json().get('access_token', None)
		print(access_token)
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
			# login(request, user)
			payload = jwt_payload_handler(user)
			response = Response()
			response['token'] = jwt_encode_handler(payload)
			return response
		else:
			# raise ValueError('Please Authorize Again')
			return Response('Please Authorize Again', status=status.HTTP_401_UNAUTHORIZED)


'''
class SocialSignUp(generics.CreateAPIView):
	queryset = User.objects.all()
	serializer_class = SocialSignUpSerializer
	# This permission is nothing special, see part 2 of this series to see its entirety
	permission_classes = (IsAuthenticatedOrCreate,)

	def create(self, request, *args, **kwargs):
		"""
		Override `create` instead of `perform_create` to access request
		request is necessary for `load_strategy`
		"""
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)

		provider = request.data['provider']

		# If this request was made with an authenticated user, try to associate this social
		# account with it
		authed_user = request.user if not request.user.is_anonymous() else None

		# `strategy` is a python-social-auth concept referencing the Python framework to
		# be used (Django, Flask, etc.). By passing `request` to `load_strategy`, PSA
		# knows to use the Django strategy
		strategy = load_strategy(request)
		# Now we get the backend that corresponds to our user's social auth provider
		# e.g., Facebook, Twitter, etc.
		backend = load_backend(strategy=strategy, name=provider, redirect_uri=None)

		if isinstance(backend, BaseOAuth1):
			# Twitter, for example, uses OAuth1 and requires that you also pass
			# an `oauth_token_secret` with your authentication request
			token = {
				'oauth_token': request.data['access_token'],
				'oauth_token_secret': request.data['access_token_secret'],
			}
		elif isinstance(backend, BaseOAuth2):
			# We're using oauth's implicit grant type (usually used for web and mobile
			# applications), so all we have to pass here is an access_token
			token = request.data['access_token']

		try:
			# if `authed_user` is None, python-social-auth will make a new user,
			# else this social account will be associated with the user you pass in
			user = backend.do_auth(token, user=authed_user)
		except AuthAlreadyAssociated:
			# You can't associate a social account with more than user
			return Response({"errors": "That social media account is already in use"},
							status=status.HTTP_400_BAD_REQUEST)

		if user and user.is_active:
			# if the access token was set to an empty string, then save the access token
			# from the request
			auth_created = user.social_auth.get(provider=provider)
			if not auth_created.extra_data['access_token']:
				# Facebook for example will return the access_token in its response to you.
				# This access_token is then saved for your future use. However, others
				# e.g., Instagram do not respond with the access_token that you just
				# provided. We save it here so it can be used to make subsequent calls.
				auth_created.extra_data['access_token'] = token
				auth_created.save()

			# Set instance since we are not calling `serializer.save()`
			serializer.instance = user
			headers = self.get_success_headers(serializer.data)
			return Response(serializer.data, status=status.HTTP_201_CREATED,
							headers=headers)
		else:
			return Response({"errors": "Error with social authentication"},
							status=status.HTTP_400_BAD_REQUEST)
'''
