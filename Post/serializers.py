from minorproject.user_profile import models
from .models import Material
from rest_framework import serializers
from .models import Material, Subject
from django.contrib.auth import get_user_model



User = get_user_model()


class SunjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        exclude = 'modified'


class MaterialSerializer(serializers.ModelSerializer):
    content = serializers.FileField()
    owner = serializers.SlugRelatedField(slug_field='username', queryset=User.objects)

    class Meta:
        model = Material
        fields = ('title', 'owner', 'content', 'subject', 'course')
