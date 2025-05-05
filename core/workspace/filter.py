from django.db.models import Q
from django_filters import rest_framework as filters
from .models import *


class NoteFilter(filters.FilterSet):
    class Meta:
        model = Note
        fields = [
        ]

    title = filters.CharFilter(field_name='title')


class NoteTemplateFilter(filters.FilterSet):
    class Meta:
        model = NoteTemplate
        fields = [
        ]

    title = filters.CharFilter(field_name='title')


class NoteAttachmentFilter(filters.FilterSet):
    class Meta:
        model = NoteAttachment
        fields = [
        ]

    title = filters.CharFilter(field_name='title')
