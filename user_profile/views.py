from rest_framework.response import Response
from rest_framework import generics, permissions, viewsets, mixins, status

#models
from .models import Profile

#serializers
from .serializers import ProfileSerializer
from Post.serializers import MaterialSerializer

from .serializers import (
    ProfileSerializer,
)
from rest_framework.views import APIView

from django.contrib.auth import get_user_model

User = get_user_model()


class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class ProfileViewSet(mixins.ListModelMixin,  #returns all profiles on the platform
                    viewsets.GenericViewSet):

    permission_classes = [UserIsOwnerOrReadOnly]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer


class MyProfileViewSet(generics.RetrieveUpdateAPIView):

    permission_classes = [UserIsOwnerOrReadOnly]
    
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

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
    
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(user=self.request.user)
        # self.check_object_permissions(self.request, obj)
        return obj


class UnlockedMaterialsAPIView(APIView):

    queryset = Profile.objects.all()
    
    def get(self, request, *args, **kwargs):
        instance = request.user.profile
        materials_unlocked_queryset = instance.materials_unlocked.all()
        serializers = MaterialSerializer(materials_unlocked_queryset, many=True)
        return Response(serializers.data)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj




























 
# class GoogleLogin(SocialLoginView):
#     authentication_classes = []
#     adapter_class = GoogleOAuth2Adapter
#     client_class = OAuth2Client
#     # callback_url = "http://127.0.0.1:8000/auth/google/"
    
#     @property
#     def callback_url(self):
#         # use the same callback url as defined in your Google app, this url
#         # must be absolute:
#         return self.request.build_absolute_uri(reverse('googlev_callback')) #http://127.0.0.1:8000/accounts/google/login/callback/

# import urllib.parse

# from django.shortcuts import get_object_or_404, redirect

# def google_callback(request):
#     params = urllib.parse.urlencode(request.GET)
#     return redirect(f'http://127.0.0.1:8000/auth/google')
