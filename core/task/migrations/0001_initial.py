# Generated by Django 3.2.4 on 2024-11-07 10:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import utils.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, max_length=500)),
                ('is_done', models.BooleanField(default=False)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Last Updated')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-pk'],
            },
            bases=(utils.models.CustomModel, models.Model),
        ),
    ]
