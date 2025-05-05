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
from notification.api.serializers import *
from notification.filter import *
from notification.models import *
from workspace.models import NoteSecurityConfig


class NotificationViewSet(CustomModelViewSet):
    model = Notification
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    disable_views = ['update', 'delete']

    def filter_queryset(self, qs):
        if not self.request.user.is_superuser:
            return Notification.objects.prefetch_related('user').filter(receivers=self.request.user)
        return super().filter_queryset(qs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['put'], detail=False, url_path='seen/(?P<notification_id>[^/.]+)')
    def seen(self, request, notification_id, *args, **kwargs):
        user = request.user
        notification: Notification = get_object_or_404(Notification, pk=notification_id)
        if user not in notification.receivers.all():
            raise Http404
        if not notification.seen_by or type(notification.seen_by) != list:
            notification.seen_by = []
        if user.id not in notification.seen_by:
            notification.seen_by.append(user.id)
        notification.save()
        return Response({
            'link': NoteSecurityConfig.objects.get(note=notification.note_id).link
        })
