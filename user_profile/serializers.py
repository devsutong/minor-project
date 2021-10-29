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
        # fields = '__all__'
        exclude = ['id']
        # fields = [  
        #             "user", "about", "created", "education_degree", "education_fromdate",
        #             "education_institute","education_specialization","education_todate",
        #             "modified","points"
        #         ]

    """
    TODO update profile and if phone Number not verified user can't update in his profile.
    """

# class PasswordChangeSerializer(serializers.Serializer):
#     old_password = serializers.CharField(max_length=128)
#     new_password1 = serializers.CharField(max_length=128)
#     new_password2 = serializers.CharField(max_length=128)

#     set_password_from_class = SetPasswordForm

#     def __init__(self, *args, **kwargs):
#         self.old_password_field_enabled = getattr(
#             settings, "OLD_PASSWORD_FIELD_ENABLED", False
#         )
#         self.logout_on_password_change = getattr(
#             settings, "LOGOUT_ON_PASSWORD_CHANGE", False
#         )
#         super(PasswordChangeSerializer, Self).__init__(*args, **kwargs)

#         self.request = self.context.get("request")
#         self.user = getattr(self.request, "user", None)

#     def validate_old_password(self, value):
#         pass

#     def validate(self, attr):
#         pass

#     def save(self):
#         self.set_password_form.save()
#         if not self.logout_on_password_change:
#             from django.contrib.auth import update_session_auth_hash
#             update_session_auth_hash(self.request, self.user)
    
# # check all ↓

# class UserMiniSerializer(serializers.ModelSerializer):
#     profile_picture = serializers.ImageField(source="profile.profile_picture")
#     gender = serializers.CharField(source="profile.gender")
#     phone_number = PhoneNumberField(source="profile.phone_number")

#     class Meta:
#         model = get_user_model()
#         fields = ["username", "profile_picture", "gender", "phone_number"]


# class AddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         exclude = "modified"


# class CreateAddressSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Address
#         exclude = ["primary", "user"]


# class PermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Permission
#         fields = ["name", "codename", "content_type"]


# class UserPermissionretriveSerializer(serializers.ModelSerializer):
#     user_permissions = PermissionSerializer(many=True, read_only=True)

#     class Meta:
#         model = UserModel
#         fields = ("user_permissions",)


# class UserPermissionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = ("user_permissions",)


# class NationalIDImageSerializer(serializers.ModelSerializer):
#     pass