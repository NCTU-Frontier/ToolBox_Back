from django.conf.urls import url
from django.conf.urls import include
from .views import *

urlpatterns = [
	url(r'/', schema_view),
	# url(r'user', user_view),
]
