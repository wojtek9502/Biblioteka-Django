# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-22 15:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0013_auto_20180922_1725'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='edition',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
