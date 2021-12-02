from django.conf.urls import url
from django.urls import include, path
from user_profile import views
from rest_framework import  routers

router = routers.DefaultRouter()
router.register(r'users/profiles', views.ProfileViewSet, basename="profiles")

urlpatterns = [
    path("", include(router.urls)),
    url("me/profile/", views.MyProfileViewSet.as_view()),
    url('materials/unlocked/', views.UnlockedMaterialsAPIView.as_view(),)
]