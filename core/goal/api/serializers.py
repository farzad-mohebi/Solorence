from rest_framework import serializers

from account.api.serializers import UserProfileSerializer
from utils.serializer import CustomSerializer
from ..models import *


class GoalSerializer(CustomSerializer):
    class Meta:
        model = Goal
        fields = model.serializer_fields()
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if validated_data.get('note') and validated_data.get('note').user != user:
            raise ValidationError('You are not allowed to update this goal')
        res = super().update(instance, validated_data)
        return res


class GoalTargetSerializer(CustomSerializer):
    class Meta:
        model = GoalTarget
        fields = model.serializer_fields()
        read_only_fields = ['user']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
