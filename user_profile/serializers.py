from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import ugettext_lazy as _
from .models import  Profile

User = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    # gender = serializers.SerializerMethodField()
    # user_avatar = Base64ImageField()

    def get_gender(self, obj):
        return obj.get_gender_display() #check https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield

    class Meta:
        model = Profile
        fields = '__all__'
        
