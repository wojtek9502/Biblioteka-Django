# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-11-02 20:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0031_auto_20181101_1652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='borrow',
            name='receive_date',
            field=models.DateField(default=datetime.datetime(2019, 1, 1, 21, 38, 30, 352076)),
        ),
        migrations.AlterField(
            model_name='userprofileinfo',
            name='house_number',
            field=models.CharField(max_length=20),
        ),
    ]
