# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 07:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0005_auto_20170921_0937'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='lockout',
        ),
        migrations.RemoveField(
            model_name='person',
            name='pwep',
        ),
        migrations.AddField(
            model_name='person',
            name='pwsv',
            field=models.BooleanField(default=True, verbose_name='PW Still Valid'),
        ),
        migrations.AddField(
            model_name='person',
            name='unlocked',
            field=models.BooleanField(default=True, verbose_name='Unlocked'),
        ),
        migrations.AlterField(
            model_name='person',
            name='pwne',
            field=models.BooleanField(default=True, verbose_name='PW Never Expires'),
        ),
    ]