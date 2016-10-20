from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rest_framework import routers
from api.views import *

router = routers.SimpleRouter()
router.register(r'users', UserViewSet, 'users')
urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^', include(router.urls)),
	url(r'^nctusignin/$', NCTUSignUp.as_view()),
	url(r'', include('rest_framework_docs.urls')),
]
