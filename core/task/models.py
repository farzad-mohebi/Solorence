from django.db import models
from rest_framework.exceptions import ValidationError
from account.models import User
from utils.models import CustomModel
from workspace.models import Note


class TaskStatus(models.IntegerChoices):
    open = 0, 'open'
    pending = 1, 'in progress'
    done = 2, 'done'


class Task(CustomModel, models.Model):
    class Meta:
        ordering = ['-pk']

    title = models.CharField(max_length=200)
    editor_data = models.JSONField(max_length=99999, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='tasks', blank=True, null=True)
    status = models.SmallIntegerField(default=TaskStatus.open, choices=TaskStatus.choices, blank=True)
    due_date = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Last Updated')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created at')

    def __str__(self):
        return self.title

    def clean(self):
        if type(self.editor_data) is not list:
            raise ValidationError(
                {"editor_data": "must be a list of blocks!"}
            )


class EventPlace(models.IntegerChoices):
    personal = 0, 'None'
    google = 1, 'Google Meet'
    zoom = 2, 'Zoom'
    location = 3, 'Location'
    link = 4, 'Link'


class Event(CustomModel, models.Model):
    class Meta:
        ordering = ['-pk']

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events')
    place = models.IntegerField(default=EventPlace.personal, choices=EventPlace.choices)
    address = models.TextField(blank=True)
    note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='events', blank=True, null=True)
    # repeat = models.IntegerField(default=0)
    start_at = models.DateTimeField(null=True, )
    end_at = models.DateTimeField(null=True, )
    guests = models.ManyToManyField(User, blank=True, related_name="invited_events")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Last Updated')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created at')

    def __str__(self):
        return self.title
