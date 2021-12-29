<<<<<<< HEAD
from django.db.models import fields
from rest_framework import serializers
from .models import Material
from user_profile.models import Profile
from django.contrib.auth import get_user_model

#serpy
import serpy


User = get_user_model()


class CategoryListSerializer(serializers.ModelSerializer):
    pass


class MaterialSerializer(serializers.ModelSerializer):
    content = serializers.FileField()
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)

    class Meta:
        model = Material
        # fields = ('title', 'owner', 'content', 'subject', 'course')
        fields = '__all__'


class MaterialMiniSerializer(serializers.ModelSerializer):
    pass

class UploadMaterialSerializer(serializers.ModelSerializer):
    # owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)
    class Meta():
        model = Material
        exclude = ['owner']

    def create(self, validated_data):
        return Material.objects.create(**validated_data)


class MaterialContentSerializer(serializers.ModelSerializer):
    class Meta():
        model = Material
        fields = ["content"]


class MaterialListSerializer(serializers.ModelSerializer):
    # owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)
    class Meta():
        model = Material
        exclude = [ "content",]

#ref: https://stackoverflow.com/questions/61537923/update-manytomany-relationship-in-django-rest-framework
class ClaimsSerializer(serializers.ModelSerializer):

    # def update(self, instance, validated_data):
    #     material_ids = validated_data.pop('materials_claimed')
    #     for material_id in material_ids:
    #         instance.materials_claimed.add(material_id)
    #     return instance

    class Meta():
        model = Profile
=======
from django.db.models import fields
from rest_framework import serializers
from .models import Material
from user_profile.models import Profile
from django.contrib.auth import get_user_model

#serpy
import serpy


User = get_user_model()


class CategoryListSerializer(serializers.ModelSerializer):
    pass


class MaterialSerializer(serializers.ModelSerializer):
    content = serializers.FileField()
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)

    class Meta:
        model = Material
        # fields = ('title', 'owner', 'content', 'subject', 'course')
        fields = '__all__'


class MaterialMiniSerializer(serializers.ModelSerializer):
    pass

class UploadMaterialSerializer(serializers.ModelSerializer):
    # owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)
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
class ClaimsSerializer(serializers.ModelSerializer):

    # def update(self, instance, validated_data):
    #     material_ids = validated_data.pop('materials_claimed')
    #     for material_id in material_ids:
    #         instance.materials_claimed.add(material_id)
    #     return instance

    class Meta():
        model = Profile
>>>>>>> chat
        fields = '__all__'