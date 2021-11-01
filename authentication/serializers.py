from rest_framework import serializers
from authentication.models import User

from dj_rest_auth.serializers import LoginSerializer as ls

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    # email = serializers.EmailField()
    # password = serializers.CharField()

    class Meta:
        model = User
        fields = ('email', 'password')
        # read_only_fields = ['token']
