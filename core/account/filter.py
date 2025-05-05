from django.db.models import Q

from account.models import User
from django_filters import rest_framework as filters


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = [
        ]
