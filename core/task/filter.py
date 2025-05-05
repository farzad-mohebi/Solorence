from django_filters import rest_framework as filters
from .models import *


class TaskFilter(filters.FilterSet):
    class Meta:
        model = Task
        fields = [
        ]

    text = filters.CharFilter(field_name='text')

