from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class Meta:
        ordering = ['-pk']

    def __str__(self):
        if len(super().__str__().split(' ')[0]):
            return super().__str__()
        return '%s object (%s)' % (self.__class__.__name__, self.pk)

    @classmethod
    def serializer_fields(cls):
        return [
            'id',
            'username',
            'password',
            'first_name',
            'last_name',
            'email',
            'is_staff',
            'is_active',
            'date_joined',
        ]
