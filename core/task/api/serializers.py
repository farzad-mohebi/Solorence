from rest_framework import serializers

from account.api.serializers import UserProfileSerializer
from utils.serializer import CustomSerializer
from ..models import *


class TaskSerializer(CustomSerializer):
    class Meta:
        model = Task
        fields = model.serializer_fields()
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        if validated_data.get('note') and validated_data.get('note').user != user:
            raise ValidationError('You are not allowed to create this task')
        return super().create(validated_data)

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if validated_data.get('note') and validated_data.get('note').user != user:
            raise ValidationError('You are not allowed to update this task')
        res = super().update(instance, validated_data)
        if res.note:
            note_data = res.note.editor_data
            if note_data and len(note_data):
                for index, block in enumerate(note_data):
                    if block.get('type') == 'task' and block.get('data') and block.get('data').get('uid') == res.id:
                        note_data[index]['data'].update(TaskSerializer(res).data)
                        del note_data[index]['data']['id']
            res.note.editor_data = note_data
            res.note.save()
        return res


class EventSerializer(CustomSerializer):
    class Meta:
        model = Event
        fields = model.serializer_fields()
        read_only_fields = ['user']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
