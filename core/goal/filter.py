from django_filters import rest_framework as filters
from .models import *


class GoalFilter(filters.FilterSet):
    class Meta:
        model = Goal
        fields = [
        ]

    text = filters.CharFilter(field_name='text')

