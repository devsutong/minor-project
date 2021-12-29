from django.contrib import admin
from django.urls import path, include


from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

#drf-yasg
from rest_framework import  permissions
from drf_yasg.views import get_schema_view
from drf_yasg import  openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Peer to Peer Learning and Material Sharing Platform",
        default_version="v1.0.0.a",
        description="RESTfull API",
        terms_of_service="https://www.example.com/tos",
        contact=openapi.Contact(email="devsutong+minor-project@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

from dj_rest_auth import urls

urlpatterns = [
    path('admin/', admin.site.urls),

    #dj_rest_auth
    path('auth/', include('dj_rest_auth.urls')),

    # path('', include(router.urls)),
    path('api/auth/', include('authentication.urls')),

    path('accounts/', include('allauth.urls')),
    path("", include('user_profile.urls')),
    path("", include("Post.urls")),

    #django-rest-framework-simplejwt.readthedocs.io
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #drf-yasg
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    #chat
    path('chat/', include('chat.urls')),
]
