from django.shortcuts import render
from rest_auth.models import TokenModel
from authentication.serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import  authenticate


from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView


# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework import response, status, permissions
# from allauth.account.views import LoginView
from dj_rest_auth.views import LoginView

class AuthUserAPIView(GenericAPIView):
    
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = LoginSerializer(user)
        return response.Response({"user": serializer.data})

class RegisterAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return response.Response(serializer.data, status=status.HTTP_201_CREATED)

        return response.Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(LoginView):
    serializer_class = LoginSerializer

    # def post(self, request):
    #     email = request.data.get('email', None)
    #     password = request.data.get('password', None)

    #     user = authenticate(username=email, password=password)

    #     if user:
    #         serializer = self.serializer_class(user)
    #         return response.Response(serializer.data, status=status.HTTP_200_OK)
        
    #     return response.Response({'message': "failed"}, status=status.HTTP_401_UNAUTHORIZED)




