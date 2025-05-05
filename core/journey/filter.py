from django_filters import rest_framework as filters
from .models import *


class JourneyFilter(filters.FilterSet):
    class Meta:
        model = Journey
        fields = [
        ]

    text = filters.CharFilter(field_name='text')

