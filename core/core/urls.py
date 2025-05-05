from django.contrib import admin
from django.contrib.auth.models import update_last_login
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from google.auth.exceptions import GoogleAuthError
from google.oauth2.id_token import verify_token
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from account.models import User
from utils.response import ResponseNotOk

schema_view = get_schema_view(
    openapi.Info(
        title="APP API",
        default_version="v1",
        description="Brief descriptions about the api",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="m.shekari79b5@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/v1/', include('account.api.routers')),
                  path('api/v1/', include('workspace.api.routers')),
                  path('api/v1/', include('notification.api.routers')),
                  path('api/v1/', include('task.api.routers')),
                  path('api/v1/', include('goal.api.routers')),
                  path('api/v1/', include('journey.api.routers')),
                  path('api/v1/', include('payment.api.routers')),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_SWAGGER:
    urlpatterns += [
        path("api-auth/", include("rest_framework.urls",
                                  namespace="rest_framework")),
        path(
            "swagger/api.json",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]

# def sign_out(request):
#     del request.session['user_data']
#     return redirect('sign_in')
