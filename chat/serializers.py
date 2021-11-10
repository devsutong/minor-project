from django.contrib.auth import get_user_model, authenticate
from rest_framework import serializers
from .models import Messages

user = get_user_model()

# User Serializer
class UserSerializer(serializers.ModelSerializer):
#    For Serializing User
    password = serializers.CharField(write_only=True)
    class Meta:
        model = user
        fields = ['username', 'password']
 
# Message Serializer
class MessageSerializer(serializers.ModelSerializer):

#   For Serializing Message
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=user.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='username', queryset=user.objects.all())
    class Meta:
        model = Messages
        fields = ['sender', 'receiver', 'message', 'timestamp']