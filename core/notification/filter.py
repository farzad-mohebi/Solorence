from django.db.models import Q
from django_filters import rest_framework as filters
from .models import *


class NotificationFilter(filters.FilterSet):
    class Meta:
        model = Notification
        fields = [
        ]

    text = filters.CharFilter(field_name='text')

