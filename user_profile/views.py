from django.urls import reverse
from rest_framework.response import Response
from rest_framework import generics, permissions, viewsets, mixins, status
from .models import Profile
from .serializers import (
    ProfileSerializer,
)

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

from django.contrib.auth import get_user_model

User = get_user_model()


class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class ProfileViewSet(mixins.ListModelMixin, 
                    # mixins.RetrieveModelMixin, 
                    # mixins.UpdateModelMixin, 
                    viewsets.GenericViewSet):

    permission_classes = [UserIsOwnerOrReadOnly]

    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    # def perform_update(self, serializer):
    #     serializer.save()

    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)



class MyProfileViewSet(
#                     mixins.ListModelMixin,
#                     mixins.RetrieveModelMixin, 
#                     mixins.UpdateModelMixin, 
#                     viewsets.GenericViewSet,
                    generics.RetrieveUpdateAPIView
                    ):

    permission_classes = [UserIsOwnerOrReadOnly]
    
    queryset = Profile.objects.all()

    #mixins
    # serializer_class = ProfileSerializer()

    # def perform_update(self, serializer):
    #     serializer.save()

    # def partial_update(self, request, *args, **kwargs):
    #     kwargs['partial'] = True
    #     return self.update(request, *args, **kwargs)

    # def list(self, request, *args, **kwargs):
    #     user = User.objects.get(pk=request.user.pk)
    #     serializer = ProfileSerializer(Profile.objects.get(user=user.pk))
    #     return Response(serializer.data)

    #generics
    serializer_class = ProfileSerializer
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(user=self.request.user)
        # self.check_object_permissions(self.request, obj)
        return obj


 
class GoogleLogin(SocialLoginView):
    authentication_classes = []
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    # callback_url = "http://127.0.0.1:8000/auth/google/"
    
    @property
    def callback_url(self):
        # use the same callback url as defined in your Google app, this url
        # must be absolute:
        return self.request.build_absolute_uri(reverse('googlev_callback')) #http://127.0.0.1:8000/accounts/google/login/callback/

import urllib.parse

from django.shortcuts import get_object_or_404, redirect

def google_callback(request):
    params = urllib.parse.urlencode(request.GET)
    return redirect(f'http://127.0.0.1:8000/auth/google')
