from django.conf.urls import url
from django.urls import include, path
from user_profile import views
from rest_framework import  routers


router = routers.DefaultRouter()


# router.register(r'my-profile', views.MyProfileViewSet, basename="my-profile")
router.register(r'profiles', views.ProfilesViewSet, basename="profiles")
urlpatterns = [
    path("", include(router.urls)),
    url("my-profile", views.MyProfileViewSet.as_view()),
    path("profile/<int:pk>/", views.ProfileListView.as_view()),
    # path('snippets/<int:pk>/', views.SnippetDetail.as_view()
]