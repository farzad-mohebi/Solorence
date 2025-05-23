# Generated by Django 3.2.4 on 2024-10-11 23:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('workspace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteSecurityConfig',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.IntegerField(choices=[(1, 'private'), (2, 'public')], default=1)),
                ('public_joiners_access', models.IntegerField(choices=[(1, 'viewer'), (2, 'commenter'), (3, 'editor')], default=1)),
                ('link', models.CharField(blank=True, max_length=64, unique=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Last Updated')),
                ('note', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='workspace.note')),
            ],
            options={
                'ordering': ['-note_id'],
            },
            bases=(utils.models.CustomModel, models.Model),
        ),
        migrations.CreateModel(
            name='NoteRequestAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.IntegerField(blank=True, choices=[(1, 'viewer'), (2, 'commenter'), (3, 'editor')], default=1)),
                ('owner_message', models.TextField(blank=True, max_length=300)),
                ('member_message', models.TextField(blank=True, max_length=300)),
                ('status', models.IntegerField(choices=[(0, 'pending'), (1, 'accepted'), (2, 'rejected')], default=0)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Last Updated')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='workspace.note')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-note_id'],
            },
            bases=(utils.models.CustomModel, models.Model),
        ),
        migrations.CreateModel(
            name='NoteAccess',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access', models.IntegerField(blank=True, choices=[(1, 'viewer'), (2, 'commenter'), (3, 'editor')], default=1)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Last Updated')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access', to='workspace.note')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='access', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-note_id'],
            },
            bases=(utils.models.CustomModel, models.Model),
        ),
    ]
