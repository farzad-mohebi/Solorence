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
from journey.api.serializers import *
from journey.filter import *
from journey.models import *
from workspace.models import NoteSecurityConfig


class JourneyViewSet(CustomModelViewSet):
    model = Journey
    queryset = Journey.objects.all()
    serializer_class = JourneySerializer
    disable_views = []

    def filter_queryset(self, qs):
        user = self.request.user
        if not user.is_superuser:
            return Journey.objects.prefetch_related('user').filter(user=user)
        return super().filter_queryset(qs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance: Journey):
        return super().perform_destroy(instance)
