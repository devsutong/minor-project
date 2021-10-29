from django.urls import include, path
# from views import  GoogleLogin
from . import views
from rest_framework import  routers
from allauth.socialaccount.providers.google import views as google_views

# from rest_auth.registration.views import RegisterView, VerifyEmailView

# router = routers.DefaultRouter()
# router.register('ids', vi********)

urlpatterns = [
    path('auth/google/', views.GoogleLogin.as_view(), name='google_login'),
    path('auth/google/', views.google_callback, name='google_callback'),
    path('auth/google/url/', google_views.oauth2_login),
    # path('', include(router.urls)),
    # path("profile/", views.ProfileViewSet.as_view({'get': 'list'}), name="profile"),
    # path("profile/", views.ProfileViewSet.as_view({'post': 'update'}), name="profile"),
    # path("profile/", views.ProfileViewSet.as_view({'get': 'list'}), name="profile"),
    # path("profile/", views.ProfileViewSet.as_view({'get': 'list'}), name="profile"),
    # path('register', RegisterAPIView.as_view()),
    # path('signup/facebook', FacebookConnectAPIView.as_view()),
    # path('signup/google', GoogleLogin.as_view()),

]