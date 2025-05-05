import datetime

from google.oauth2.service_account import Credentials
from google.apps import meet_v2
from django.conf import settings
from django.http import JsonResponse, Http404
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied, NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from account.api.serializers import UserProfileSerializer
from utils.response import ResponseOk, BadRequest
from utils.viewset import CustomModelViewSet
from task.api.serializers import *
from task.filter import *
from task.models import *
from workspace.models import NoteSecurityConfig


class TaskViewSet(CustomModelViewSet):
    model = Task
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    disable_views = []

    def filter_queryset(self, qs):
        user = self.request.user
        if not user.is_superuser:
            return Task.objects.prefetch_related('user').filter(user=user)
        return super().filter_queryset(qs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance: Task):
        if instance.note:
            note_data = instance.note.editor_data
            if note_data and len(note_data):
                for index, block in enumerate(note_data):
                    if block.get('type') == 'task' and block.get('data') and \
                            block.get('data').get('uid') == instance.id:
                        del instance.note.editor_data[index]
            instance.note.save()
        return super().perform_destroy(instance)


class EventViewSet(CustomModelViewSet):
    model = Event
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    disable_views = []

    def filter_queryset(self, qs):
        user = self.request.user
        if not user.is_superuser:
            return Event.objects.prefetch_related('user').filter(user=user)
        return super().filter_queryset(qs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
