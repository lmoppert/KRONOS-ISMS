# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 15:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0012_workstation_category'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ComputerCateogry',
            new_name='ComputerCategory',
        ),
    ]