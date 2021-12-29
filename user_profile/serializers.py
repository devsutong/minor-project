<<<<<<< HEAD
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
        
=======
# from _typeshed import Self
# from typing_extensions import Required
from django.contrib.auth import get_user_model, authenticate
from django.core.checks import messages
from rest_framework import serializers, exceptions
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from allauth.account.models import EmailAddress
from rest_auth.registration.serializers import RegisterSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from drf_extra_fields.fields import  Base64ImageField
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import Permission

from rest_framework.fields import CharField
from rest_framework.validators import UniqueValidator

from .models import  Profile

User = get_user_model()

# class DeactivateUserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DeactivateUser
#         exclude = ["deactive", "user"]


class ProfileSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field="username", read_only=True)
    # gender = serializers.SerializerMethodField()
    # user_avatar = Base64ImageField()

    def get_gender(self, obj):
        return obj.get_gender_display() #check https://www.django-rest-framework.org/api-guide/fields/#serializermethodfield

    class Meta:
        model = Profile
        fields = '__all__'
        # exclude = ['id']
        # fields = [  
        #             "user", "about", "created", "education_degree", "education_fromdate",
        #             "education_institute","education_specialization","education_todate",
        #             "modified","points"
        #         ]

    """
    TODO update profile and if phone Number not verified user can't update in his profile.
    """
>>>>>>> chat
