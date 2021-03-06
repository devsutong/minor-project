from django.db.models import fields
from rest_framework import serializers
from .models import Material
from user_profile.models import Profile
from django.contrib.auth import get_user_model
import serpy


User = get_user_model()


class CategoryListSerializer(serializers.ModelSerializer):
    pass


class MaterialSerializer(serializers.ModelSerializer):
    content = serializers.FileField()
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)

    class Meta:
        model = Material
        fields = '__all__'


class MaterialMiniSerializer(serializers.ModelSerializer):
    pass

class UploadMaterialSerializer(serializers.ModelSerializer):
    class Meta():
        model = Material
        exclude = ['owner']

    def create(self, validated_data):
        return Material.objects.create(**validated_data)


class MaterialDetailSerializer(serializers.ModelSerializer):
    pass


class MaterialListSerializer(serializers.ModelSerializer):

    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)
    class Meta():
        model = Material
        
        exclude = [ "content",]

#ref: https://stackoverflow.com/questions/61537923/update-manytomany-relationship-in-django-rest-framework
class UnlocksSerializer(serializers.ModelSerializer):

    class Meta():
        model = Profile
        fields = '__all__'