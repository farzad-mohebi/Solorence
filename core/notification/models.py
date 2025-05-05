from django.db import models
from rest_framework.exceptions import ValidationError
from account.models import User
from utils.models import CustomModel
from workspace.models import Note


class Notification(CustomModel, models.Model):
    class Meta:
        ordering = ['-pk']

    text = models.TextField(max_length=1000, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sends')
    receivers = models.ManyToManyField(User, related_name="notifications")
    note = models.ForeignKey(Note, on_delete=models.CASCADE, null=True, blank=True, related_name='notifications')
    seen_by = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created at')

    def __str__(self):
        return self.text

    def clean(self):
        if type(self.seen_by) is not list:
            raise ValidationError(
                {"editor_data": "must be a list of blocks!"}
            )
