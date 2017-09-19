# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-15 14:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=200)),
                ('countrycode', models.CharField(max_length=5)),
                ('country', models.CharField(max_length=200)),
                ('department', models.CharField(max_length=200)),
                ('employee', models.CharField(max_length=50)),
                ('location', models.CharField(max_length=50)),
                ('mail', models.CharField(max_length=200)),
                ('fax', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('mobile', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=400)),
            ],
        ),
    ]
