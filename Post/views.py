from rest_framework import serializers
from rest_framework import generics
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status

from .models import Material

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
    MaterialDetailSerializer,
    ClaimsSerializer
)

from user_profile.models import Profile

from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()

class UserIsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.id == request.user.id


class MyMaterialViewset(  mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [UserIsOwnerOrReadOnly]
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer




class MaterialListAPIView(ListAPIView):
    serializer_class = MaterialListSerializer
    search_fields = ['title']
    filter_backends = (filters.SearchFilter, 
                        filters.OrderingFilter,)
    search_fields = ['title']
    order_fields = ['id'] #check 
    queryset = Material.objects.all()

 
class UploadMatertialView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_serializer = UploadMaterialSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save(owner=request.user)
            
            return Response(file_serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status.HTTP_400_BAD_REQUEST)


# from user_profile.serializers import ProfileSerializer

class ClaimMaterialView( generics.UpdateAPIView,
                        # mixins.UpdateModelMixin,
                        # mixins.RetrieveModelMixin,
                        # viewsets.GenericViewSet
                        ):
    queryset = Profile.objects.all()
# 
    serializer_class = ClaimsSerializer

    def patch(self, request, *args, **kwargs):
        material_ids = request.data.get('materials_claimed')
        for material_id in material_ids:
            self.get_object().materials_claimed.add(material_id)
        return Response(status.HTTP_201_CREATED)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below
        obj = queryset.get(user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj

        
             





