from django.contrib.auth.models import User, AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from datetime import datetime


class CustomUserManager(BaseUserManager):
	def create_user(self, username, email, password=None):
		if not email:
			raise ValueError('Email is required')
		user = self.model(
			username=username,
			email=self.normalize_email(email),
		)
		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, username, email, password=None):
		if not email:
			raise ValueError('Email is required')
		user = self.model(
			username=username,
			email=self.normalize_email(email),
		)
		user.set_password(password)
		user.is_active = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

	# def get_queryset(self):
	# 	return super(BaseUserManager, self).get_queryset()


# Create your models here.
class CustomUser(AbstractBaseUser, PermissionsMixin):
	username = models.CharField('Username', max_length=30, unique=True)
	student_id = models.CharField('StudentId', max_length=10)
	email = models.EmailField('Email', unique=True)
	name = models.CharField('Name', max_length=30)
	is_staff = models.BooleanField('staff_status', default=False)
	is_active = models.BooleanField('active_status', default=True)
	date_joined = models.DateTimeField('join date', auto_now=datetime.now)

	objects = CustomUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	class Meta:
		verbose_name = 'user'
		verbose_name_plural = 'users'

	def __str__(self):
		return self.username

	def get_short_name(self):
		return self.name

	def get_full_name(self):
		return self.name
