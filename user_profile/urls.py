from django.urls import include, path
from user_profile import views
from rest_framework import  routers


router = routers.DefaultRouter()


router.register(r'my-profile', views.MyProfileViewSet)
router.register(r'profiles', views.ProfileViewSet)

urlpatterns = [
    path("", include(router.urls)),
]