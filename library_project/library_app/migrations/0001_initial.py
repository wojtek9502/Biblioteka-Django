# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-15 15:08
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=200)),
                ('last_name', models.CharField(max_length=200)),
                ('country', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', models.CharField(max_length=30, unique=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, default='')),
                ('publish_year', models.DateField()),
                ('edition', models.IntegerField(default=1)),
                ('is_borrowed', models.BooleanField(default=False)),
                ('slug', models.SlugField(allow_unicode=True, unique=True)),
                ('authors', models.ManyToManyField(related_name='book_authors', to='library_app.Author')),
            ],
        ),
        migrations.CreateModel(
            name='BookCopy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.Book')),
            ],
        ),
        migrations.CreateModel(
            name='Borrow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('borrow_date', models.DateField(auto_now=True)),
                ('receive_date', models.DateField()),
                ('book_copy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library_app.BookCopy')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
            ],
        ),
        migrations.CreateModel(
            name='PublishingHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=400)),
                ('city', models.CharField(max_length=300)),
                ('street', models.CharField(max_length=300)),
                ('house_number', models.CharField(max_length=20)),
                ('postal_code', models.CharField(max_length=9)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='book_categories', to='library_app.Category'),
        ),
        migrations.AddField(
            model_name='book',
            name='publishing_house',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publishing_houses', to='library_app.PublishingHouse'),
        ),
    ]
