# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-03-24 19:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gallery', '0003_remove_picture_is_favorite'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='is_favorite',
            field=models.BooleanField(default=False),
        ),
    ]
