# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-16 09:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0004_auto_20180915_1803'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='image_url',
            field=models.URLField(default=''),
        ),
    ]
