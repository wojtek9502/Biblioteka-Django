# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-11 13:13
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0038_auto_20181110_1735'),
    ]

    operations = [
        migrations.AddField(
            model_name='borrow',
            name='is_date_exceeded',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='borrow',
            name='receive_date',
            field=models.DateField(default=datetime.datetime(2019, 1, 10, 14, 13, 35, 842329), verbose_name='Data oddania'),
        ),
    ]
