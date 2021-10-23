# from decimal import Context
# from allauth.account import adapter
# from django.conf import settings
# from django.views.decorators.debug import sensitive_post_parameters
# from django.utils.decorators import  method_decorator
# from .models import DeactivateUser
# from rest_framework.views import  APIView
# from rest_framework.response import Response
# from rest_framework import permissions, serializers, status, viewsets
# from .models import Profile, Address, SMSVerification, DeactivateUser
# from .serializers import (
#     ProfileSerializer,
#     UserSerializer,
#     AddressSerializer,
#     CreateAddressSerializer,
#     # SMSVerificationSerializer,
#     SMSPinSerializer,
#     DeactivateUserSerializer,
#     PermissionSerializer,
#     PasswordChangeSerializer,
#     UserPermissionSerializer,
#     NationalIDImageSerializer,
# )

# from rest_framework.generics import (
#     ListAPIView,
#     RetrieveAPIView,
#     CreateAPIView,
#     GenericAPIView,
#     RetrieveUpdateAPIView,
#     UpdateAPIView
# )
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
# from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
# from allauth.socialaccount.providers.oauth2.client import OAuth2Client
# from rest_auth.registration.views import SocialConnectView, SocialLoginView
# from rest_auth.social_serializers import TwitterConnectSerializer

# from django.contrib.auth.models import User

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

# class ProfileAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, pk):
#         profile = Profile.objects.get(pk=pk)
#         serializers = ProfileSerializer(profile, context={"request": request})
#         return Response(serializers.data, status.HTTP_200_OK)
    
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

# class GoogleLogin(SocialLoginView):
#     adapter_class = GoogleOAuth2Adapter
#     client_class = OAuth2Client
#     callback_url = "https://www.google.com"



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