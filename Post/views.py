from urllib import request
from rest_framework import generics
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
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
    get_object_or_404,
)

from .serializers import (
    MaterialListSerializer,
    MaterialSerializer,
    UploadMaterialSerializer,
    UnlocksSerializer
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


class MyMaterialViewset(ListAPIView):
    # permission_classes = [UserIsOwnerOrReadOnly]
    serializer_class = MaterialSerializer

    def get(self, request, *args, **kwargs):
        self.queryset = Material.objects.get_mymaterials(request.user)
        return super().get(request, *args, **kwargs)



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

class UnlockMaterialView( generics.UpdateAPIView):
    
    queryset = Profile.objects.all()
# 
    serializer_class = UnlocksSerializer

    def patch(self, request, *args, **kwargs):
        material_ids = request.data.get('materials_unlocked')
        for material_id in material_ids:
            self.get_object().materials_unlocked.add(material_id)
        return Response(status.HTTP_201_CREATED)

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        # make sure to catch 404's below??
        obj = queryset.get(user=self.request.user)
        self.check_object_permissions(self.request, obj)
        return obj
