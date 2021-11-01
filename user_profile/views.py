# from decimal import Context
# from allauth.account import adapter
# from django.conf import settings
# from django.views.decorators.debug import sensitive_post_parameters
# from django.utils.decorators import  method_decorator
# from .models import DeactivateUser
from django.urls import reverse
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework import permissions, serializers, status, viewsets, mixins
from .models import Profile #, Address SMSVerification, DeactivateUser
from .serializers import (
    ProfileSerializer,
    # UserSerializer,
#     AddressSerializer,
#     CreateAddressSerializer,
#     # SMSVerificationSerializer,
#     SMSPinSerializer,
#     DeactivateUserSerializer,
#     PermissionSerializer,
#     PasswordChangeSerializer,
#     UserPermissionSerializer,
#     NationalIDImageSerializer,
)


from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    GenericAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView
)
# from rest_auth.views import (
#     LoginView,
#     PasswordResetView,
#     PasswordResetConfirmView,
#     PasswordChangeView,
#     LogoutView
# )

# from rest_auth.registration.views import RegisterView
# from rest_auth.app_settings import JWTSerializer
# from rest_auth.utils import jwt_encode

# from allauth.account.models import EmailAddress, EmailConfirmationHMAC
# from allauth.account.views import ConfirmEmailView
# from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
# from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
# from rest_auth.social_serializers import TwitterConnectSerializer

# from django.contrib.auth.models import User

from django.contrib.auth import get_user_model

User = get_user_model()

# sensitive_post_parameters_m = method_decorator( #Convert a function decorator into a method decorator
#     sensitive_post_parameters("password1", "password2")
# )

# class DeactivateUserView(CreateAPIView):
#     pass

# class canselDeactivateAPIView(APIView):
#     pass

# class LoginAPIView(LoginView):
#     queryset = ""

#     def get_response(self):
#         serializer_class = self.get_response_serializer()
#         if getattr(settings, "REST_USE_JWT", False):
#             data = {
#                 "user": self.user,
#                 "token": self.token,
#             }
#             serializer = serializer_class(
#                 instance=data, context={"request":self.request}
#             )
#         else:
#             serializer = serializer_class(
#                 instance=self.token, context={"request", self.request}
#             )
#         response = Response(serializer.data, status=status.HTTP_200_OK)

#         deactivate = DeactivateUser.objects.filter(user=self.user, deactive=True)
#         if deactivate:
#             deactivate.update(deactive=False)
#         return Response

#     def post(self, request, *args, **kwargs):
#         self.request  = self.request
#         self.serializer = self.get_serializer(
#             data=self.request.data, context={"request": request}
#         )
#         self.serializer.is_valid(raise_exception=True)
#         self.login()
#         return self.get_response()

# class RegisterAPIView(RegisterView):
#     @sensitive_post_parameters_m #m for method decorator, hides sensitive data (for eg. in logging)
#     def dispatch(self, *args, **kwargs): #dispatch get? post?
#         return super(RegisterAPIView, self).dispatch(*args, **kwargs) 
    
#     def get_response_data(self, user):
#         if getattr(settings, "REST_USE_JWT", False):
#             data = {"user": user, "token": self.token}
#         return JWTSerializer(data).data
    
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = self.perform_create(serializer) #mixins
#         headers = self.get_success_headers(serializer.data) #mixins

#         return Response (
#             self.get_response_data(user),
#             status=status.HTTP_201_CREATED,
#             headers=headers,
#         )

#     def perform_create(self, serializer):
#         user = serializer.save(self.request)
#         if (getattr(settings, "REST_USE_JWT", False)):
#             self.token = jwt_encode(user)
        
#         email = EmailAddress.objects.get(email=user.email, user=user)
#         confirmation = EmailConfirmationHMAC(email)
#         key = confirmation.Key
#         #TODO Send Mail conf9ormation here
#         # send_register_mail.delay(user. key)
#         print("account-confiem-email/" + key)
#         return user

# # class GoogleSocialAuthView(GenericAPIView):
# #     serializer_class = GoogleSocialAuthSerializer


# class ResendSMSAPIView(GenericAPIView):
#     pass

# class VerifySMSAPIView(APIView):
#     pass

class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class ProfileViewSet(mixins.ListModelMixin, 
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    viewsets.GenericViewSet):

    permission_classes = [UserIsOwnerOrReadOnly]
    # permission_classes = [permissions.AllowAny]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)



class MyProfileViewSet(mixins.ListModelMixin,
                    mixins.RetrieveModelMixin, 
                    mixins.UpdateModelMixin, 
                    viewsets.GenericViewSet):
    

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer()

    def perform_update(self, serializer):
        serializer.save()

    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.user.pk)
        serializer = ProfileSerializer(Profile.objects.get(user=user.pk))
        return Response(serializer.data)



    # def get(self, request): #pk?
    # #     pk = 6
    # #     print(pk)
    #     # profile = Profile.objects.get(pk=pk)
    #     profile = request.user.profiles
    #     serializers = ProfileSerializer(profile, context={"request": request})
    #     return Response(serializers.data, status.HTTP_200_OK)

    # def post(self, request):
    #     serializer = ProfileSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save(user=request.user, primary=True)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class UserDetailView(RetrieveAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#     lookup_field = "username"

# class ListAddressAPIView(ListAPIView):
#     pass

# class AddressDetailView(RetrieveAPIView):
#     pass

# class CreateAddressAPIView(CreateAPIView): #Corc
#     pass

# class FacebookConnectAPIView(SocialLoginView):
#     adapter_class = FacebookOAuth2Adapter
    
# class TwitterConnectView(SocialLoginView): 
#     serializer_class = TwitterConnectSerializer
#     adapter_class = TwitterOAuthAdapter

class GoogleLogin(SocialLoginView):
    # permission_classes = [permissions.AllowAny,]
    authentication_classes = []
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    # callback_url = "http://127.0.0.1:8000/auth/google/"
    
    @property
    def callback_url(self):
        # use the same callback url as defined in your GitHub app, this url
        # must be absolute:
        return self.request.build_absolute_uri(reverse('googlev_callback')) #http://127.0.0.1:8000/accounts/google/login/callback/

import urllib.parse

from django.shortcuts import get_object_or_404, redirect

def google_callback(request):
    params = urllib.parse.urlencode(request.GET)
    return redirect(f'http://127.0.0.1:8000/auth/google')


# http://127.0.0.1:8000/auth/google/url

# class PasswordResetView(APIView):
#     pass

# class PasswordResetConfirmView(GenericAPIView):
#     permission_classes = (permissions.AllowAny, )
#     serializer_class = PasswordResetConfirmView

#     pass

# class PasswordChangeView(GenericAPIView):
#     pass

# class VerifyEmailView(APIView, ConfirmEmailView):
#     pass

# class RetrievePermissionView(RetrieveAPIView):
#     pass

# class UpdatePermissionView(UpdateAPIView):
#     pass

# #check