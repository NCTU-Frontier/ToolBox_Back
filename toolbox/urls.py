from django.conf.urls import url
from django.contrib import admin
from django.conf.urls import include
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response, schemas, renderers, routers
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from api.views import *

# @api_view()
# @renderer_classes([OpenAPIRenderer, SwaggerUIRenderer, renderers.CoreJSONRenderer])
# def schema_view(request):
# 	generator = schemas.SchemaGenerator(title='ToolBox API')
# 	return response.Response(generator.get_schema(request=request)

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, 'users')
# router.register(r'nctusignin')
urlpatterns = [
	url(r'^admin/', admin.site.urls),
	url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
	url(r'^', include(router.urls)),
	url(r'^nctusignin/$', NCTUSignUp.as_view()),

	# url(r'^', include('api.urls', namespace="api")),
]
