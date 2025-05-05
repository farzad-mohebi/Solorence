import datetime

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from account.api.serializers import UserProfileSerializer
from utils.serializer import CustomSerializer
from ..models import *


class JourneySerializer(CustomSerializer):
    class Meta:
        model = Journey
        fields = model.serializer_fields()
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        if not validated_data.get('action_at'):
            validated_data['action_at'] = datetime.datetime.now()
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if not validated_data.get('action_at'):
            validated_data['action_at'] = datetime.datetime.now()
        res = super().update(instance, validated_data)
        return res
