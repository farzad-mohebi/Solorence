# Generated by Django 3.2.4 on 2024-11-15 12:25

from django.db import migrations, models
import django.db.models.deletion
import utils.models
import uuid
import workspace.models


class Migration(migrations.Migration):

    dependencies = [
        ('workspace', '0006_auto_20241020_1112'),
    ]

    operations = [
        migrations.CreateModel(
            name='NoteAttachment',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to=workspace.models.note_directory_path)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Last Updated')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created at')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='workspace.note')),
            ],
            options={
                'ordering': ['-note_id'],
            },
            bases=(utils.models.CustomModel, models.Model),
        ),
    ]
