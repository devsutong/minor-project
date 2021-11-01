from django.db.models import fields
from rest_framework import serializers
from .models import Material
from django.contrib.auth import get_user_model



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
        exclude = ['vote_up', 'vote_down', 'owner']

    def create(self, validated_data):
        return Material.objects.create(**validated_data)


class MaterialDetailSerializer(serializers.ModelSerializer):
    pass

class MaterialViewSerializer(serializers.ModelSerializer):
    pass
