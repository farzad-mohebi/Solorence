from rest_framework import serializers

from account.api.serializers import UserProfileSerializer
from utils.mail import MailService
from utils.serializer import CustomSerializer
from ..models import *


class NotificationSerializer(CustomSerializer):
    is_seen = serializers.SerializerMethodField(read_only=True, allow_null=True)
    user = UserProfileSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Notification
        fields = model.serializer_fields() + ['is_seen']
        read_only_fields = ['user']

    def create(self, validated_data):
        if not validated_data['note']:
            raise ValidationError('note undefined!')
        if validated_data['note'].user != validated_data['user']:
            raise ValidationError('this note is unavailable!')
        res: Notification = super().create(validated_data)
        MailService().send_notification(res)
        return res

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    def get_is_seen(self, obj):
        user = self.context['request'].user
        return user.id in obj.seen_by
