# Generated by Django 5.0.4 on 2024-04-20 11:23

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WakeUpApp', '0002_events'),
    ]

    operations = [
        migrations.AddField(
            model_name='events',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='events',
            name='name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
