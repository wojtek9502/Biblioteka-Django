# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-18 17:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('library_app', '0011_book_add_by'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='add_by',
        ),
    ]