from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'username', 'email', 'student_id', 'password')
		# write_only_fields = ('password',)
		extra_kwargs = {
			'url': {'view_name': 'users-detail', 'lookup_field': 'username',},
			'password': {'write_only': True}
		}


class NCTUSignUpSerializer:
	code = serializers.CharField('code')