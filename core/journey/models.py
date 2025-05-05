from django.db import models
from account.models import User
from utils.models import CustomModel


class Journey(CustomModel, models.Model):
    class Meta:
        ordering = ['-pk']

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='journeys')
    action_at = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created at')

    def __str__(self):
        return self.title
