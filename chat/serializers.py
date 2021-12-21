from django.db.models import fields
from rest_framework import serializers
from .models import Messages, ReportedMessages, Attachment
from django.contrib.auth import get_user_model
from . validators import blacklist_validator, ValidationError
from .utils import get_user_info_from_instance

User = get_user_model()


class UploadAttachmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Attachment
        fields = ['id', 'file']
    
    def validate(self, attrs):
        attrs['owner'] = self.context['request'].user
        return super().validate(attrs)


class MaterialSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    sender = serializers.PrimaryKeyRelatedField(read_only=True)
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    message = serializers.CharField(validators=(blacklist_validator,), required=False)
    datetime = serializers.DateTimeField(read_only=True)
    read = serializers.BooleanField(read_only=True)
    attachments = serializers.PrimaryKeyRelatedField(many=True, queryset=Attachment.objects.all())

    def to_representation(self, instance): #https://www.django-rest-framework.org/api-guide/serializers/#overriding-serialization-and-deserialization-behavior
        data = super().to_representation(instance)
        data['sender'] = get_user_info_from_instance(instance.sender)
        data['reciever'] = get_user_info_from_instance(instance.reciever)
        data['attachments'] = [{
            'file': self.context['request'].build_absolute_uri(i.file.url)
        } for i in instance.attachments.all()]
        return data

    def create(self, validated_data):
        mes = Messages.objects.send_message(**validated_data, sender=self.context['request'].user)
        mes.attachmemts.set(validated_data['attachments'])
        mes.save()
        return mes

class GetChatSerializer(serializers.Serializer):
    user = serializers.IntegerField()
    unread_messages = serializers.IntegerField()
    last_message = serializers.SerializerMethodField()

    def to_representation(self, instance):
        data =  super().to_representation(instance)
        data['user'] = get_user_info_from_instance(User.objects.get(id=data['user']))
        return data

    def get_last_message(self, instance):
        message = Messages.objects.get(id=instance['last_message_id'])
        response = {
                'message': message.message,
                'datetime': message.datetime,
                'sender': get_user_info_from_instance(message.sender),
                'reciever': get_user_info_from_instance(message.reciever)
        }
        return response

        
