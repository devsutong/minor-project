from django.urls import  path
from . import views

from django.urls import path, re_path
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView, ConfirmEmailView

# from .views import LoginAPIView


urlpatterns = [
    # path('register', views.RegisterAPIView.as_view(), name="register"),
    # path('login', views.LoginAPIView.as_view(), name='login'),
#     path('user', views.AuthUserAPIView.as_view(), name='user'),
    # path('google-login', views.GoogleLogin.as_view(), name='google-login'),

    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('register/', RegisterView.as_view()),
#     path('login/', LoginAPIView.as_view()),
#     path('logout/', LogoutViewAPI.as_view()),

    path('verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/',
         VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
            VerifyEmailView.as_view(), name='account_confirm_email'),
]