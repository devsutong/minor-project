from django.db.models import fields
from rest_framework import serializers
from .models import Messages, ReportedMessages, Attachment
from django.contrib.auth import get_user_model
from .validators import blacklist_validator, ValidationError


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
