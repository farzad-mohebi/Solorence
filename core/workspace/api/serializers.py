from rest_framework import serializers

from account.api.serializers import UserProfileSerializer
from utils.serializer import CustomSerializer
from ..models import *


class NoteSerializer(CustomSerializer):
    class Meta:
        model = Note
        fields = model.serializer_fields()
        read_only_fields = ['user']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class NoteTemplateSerializer(CustomSerializer):
    class Meta:
        model = NoteTemplate
        fields = model.serializer_fields()
        read_only_fields = ['user']

    def create(self, validated_data):
        return super().create(validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class NoteAttachmentSerializer(CustomSerializer):
    class Meta:
        model = NoteAttachment
        fields = ['id', 'title', 'note', 'image', ]
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        note: Note = validated_data['note']
        if note.user != user:
            raise ValidationError('You do not have permission to add attachments to this note')
        return super().create(validated_data)


class NoteLinkSerializer(CustomSerializer):
    link = serializers.SerializerMethodField()

    class Meta:
        model = Note
        fields = ['id', 'title', 'link']

    def get_link(self, obj: Note):
        return obj.get_settings().link


class NoteSecurityConfigSerializer(CustomSerializer):
    class Meta:
        model = NoteSecurityConfig
        fields = model.serializer_fields()
        read_only_fields = ['note', 'link']


class NoteAccessSerializer(CustomSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = NoteAccess
        fields = model.serializer_fields()
        read_only_fields = ['note', 'user']


class NoteRequestAccessSerializer(CustomSerializer):
    user = UserProfileSerializer()

    class Meta:
        model = NoteRequestAccess
        fields = model.serializer_fields()
        read_only_fields = ['note', 'user']
