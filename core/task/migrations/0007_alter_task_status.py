# Generated by Django 3.2.4 on 2024-11-15 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0006_auto_20241115_1050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.SmallIntegerField(blank=True, choices=[(0, 'open'), (1, 'in progress'), (2, 'done')], default=0),
        ),
    ]
