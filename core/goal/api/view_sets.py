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
from goal.api.serializers import *
from goal.filter import *
from goal.models import *
from workspace.models import NoteSecurityConfig


class GoalViewSet(CustomModelViewSet):
    model = Goal
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer
    disable_views = []

    def filter_queryset(self, qs):
        user = self.request.user
        if not user.is_superuser:
            return Goal.objects.prefetch_related('user').filter(user=user)
        return super().filter_queryset(qs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_destroy(self, instance: Goal):
        return super().perform_destroy(instance)


class GoalTargetViewSet(CustomModelViewSet):
    model = GoalTarget
    queryset = GoalTarget.objects.all()
    serializer_class = GoalTargetSerializer
    disable_views = ['list']

    def filter_queryset(self, qs):
        user = self.request.user
        if self.action == 'goal':
            return GoalTarget.objects.filter(user=user, goal_id=self.kwargs['goal_id'])
        if not user.is_superuser:
            return GoalTarget.objects.prefetch_related('user').filter(user=user)
        return super().filter_queryset(qs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(methods=['get'], detail=False, serializer_class=GoalTargetSerializer,
            permission_classes=[permissions.IsAuthenticated], url_path='goal/(?P<goal_id>[^/.]+)')
    def goal(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
