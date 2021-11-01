from rest_framework import serializers
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import status


from .serializers import (
    CategoryListSerializer,
    MaterialSerializer,
    MaterialMiniSerializer,
    UploadMaterialSerializer,
    MaterialDetailSerializer,
    MaterialViewSerializer
)

from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()
 
class UploadMatertialView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_serializer = UploadMaterialSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save(owner=request.user)
            
            return Response(file_serializer.data, status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status.HTTP_400_BAD_REQUEST)

