from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg
from rest_framework.exceptions import ValidationError
from account.models import User
from utils.models import CustomModel
from workspace.models import Note


class Goal(CustomModel, models.Model):
    class Meta:
        ordering = ['-pk']

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='goals')
    progress = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(101), ])
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Last Updated')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created at')

    def __str__(self):
        return self.title

    def update_progress(self):
        self.progress = self.targets.all().aggregate(Avg('progress')).get('progress__avg') or 0
        self.save()


class GoalTargetStatus(models.IntegerChoices):
    open = 0, 'open'
    pending = 1, 'in progress'
    done = 2, 'done'


class GoalTarget(CustomModel, models.Model):
    class Meta:
        ordering = ['-pk']

    title = models.CharField(max_length=200)
    description = models.TextField(max_length=500, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='targets')
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name='targets')
    progress = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(101), ])
    status = models.SmallIntegerField(default=GoalTargetStatus.open, choices=GoalTargetStatus.choices, blank=True)
    deadline_at = models.DateField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Last Updated')
    created_at = models.DateTimeField(auto_now_add=True, blank=True, verbose_name='Created at')

    def __str__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.status != GoalTargetStatus.done and self.progress == 100:  # if Task is 100%
            self.status = GoalTargetStatus.done
        super().save(force_insert, force_update, using, update_fields)
        self.goal.update_progress()

    def delete(self, using=None, keep_parents=False):
        res = super().delete(using, keep_parents)
        self.goal.update_progress()
        return res
