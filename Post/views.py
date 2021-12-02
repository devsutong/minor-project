from rest_framework import serializers
from rest_framework import generics
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status

#models
from .models import Material

from activities.models import Activity


from rest_framework import viewsets, mixins
from rest_framework import permissions

#search
from rest_framework import filters

from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    DestroyAPIView,
    get_object_or_404,
)

from .serializers import (
    MaterialListSerializer,
    CategoryListSerializer,
    MaterialSerializer,
    MaterialMiniSerializer,
    UploadMaterialSerializer,
    MaterialContentSerializer,
    ClaimsSerializer
)

from user_profile.models import Profile
from user_profile.serializers import ProfileSerializer

from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id

class UserIsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id

# class MyMaterialViewset(  mixins.ListModelMixin,
#                         mixins.RetrieveModelMixin,
#                         mixins.UpdateModelMixin,
#                         viewsets.GenericViewSet):
#     permission_classes = [UserIsOwnerOrReadOnly]
#     queryset = Material.objects.all()
#     serializer_class = MaterialSerializer


class MaterialListAPIView(ListAPIView):
    serializer_class = MaterialListSerializer
    search_fields = ['title']
    filter_backends = (filters.SearchFilter, 
                        filters.OrderingFilter,)
    search_fields = ['title']
    order_fields = ['id'] #check 
    queryset = Material.objects.all()

 
class UploadMatertialView(generics.UpdateAPIView):

    parser_classes = [MultiPartParser, FormParser]
    queryset = Profile.objects.all()

    def post(self, request, *args, **kwargs):
        file_serializer = UploadMaterialSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save(owner=request.user)
            #logic
            instance = self.get_object()
            instance.points  += Profile.UPLOAD_POINT
            instance.save()
            return Response(file_serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status.HTTP_400_BAD_REQUEST)
    
    #added
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

class UploadsListAPIView(APIView):
    permission_classes = [UserIsOwnerOrReadOnly]

    def get(self, request, *args, **kwargs):
        queryset = Material.objects.all().filter(owner=request.user)
        serializer = MaterialListSerializer(queryset, many=True)
        # return self.list(request, *args, **kwargs)
        return Response(serializer.data)


class UnlockMaterialView(generics.UpdateAPIView): #action

    queryset = Profile.objects.all()
    serializer_class = ClaimsSerializer

    def patch(self, request, *args, **kwargs):
        profile_instance = self.get_object()
        if profile_instance.points > 5:
            profile_instance.points += Profile.UNLOCK_POINT
            profile_instance.save()
            material_ids = request.data.get('material_id')
            for material_id in material_ids:
                self.get_object().materials_unlocked.add(material_id)
            return Response(status.HTTP_201_CREATED)
        else:
            return Response(r"Not Enough Points", status.HTTP_400_BAD_REQUEST)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

class UnlockedMaterialsAPIView(APIView):

    def get(self, request, *args, **kwargs):
        profile_instance = Profile.objects.get(user=request.user)
        queryset = profile_instance.materials_unlocked.all()
        serializer = MaterialListSerializer(queryset, many=True)
        # return self.list(request, *args, **kwargs)
        return Response(serializer.data)


class MaterialContentAPIView(APIView):

    def get(self, request, *args, **kwargs):
        material = Material.objects.get(uuid=request.data.get('uuid'))
        if (material.owner == request.user):
            serializer = MaterialContentSerializer(material)
            return Response(serializer.data)
        else:
            return Response(status.HTTP_204_NO_CONTENT)


class UpVoteAPIView(APIView):

    queryset = Material.objects.all()

    def post(self, request):
        post = Material.objects.get(pk=request.data.get('material_id'))
        Activity.objects.upvote(post, request.user)
        return Response(post.up_vote.count(), status.HTTP_200_OK)
    

class DownVoteAPIView(APIView):

    queryset = Material.objects.all()

    def post(self, request):
        post = Material.objects.get(pk=request.data.get('material_id'))
        Activity.objects.downvote(post, request.user)
        return Response(post.down_vote.count(), status.HTTP_200_OK)


             





