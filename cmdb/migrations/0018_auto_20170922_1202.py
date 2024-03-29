# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-22 10:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0017_auto_20170922_1152'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Country Name')),
                ('token', models.CharField(max_length=3, verbose_name='Country Token')),
            ],
            options={
                'verbose_name': 'Country',
                'verbose_name_plural': 'Countries',
            },
        ),
        migrations.RemoveField(
            model_name='location',
            name='country',
        ),
        migrations.AddField(
            model_name='location',
            name='nation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.Country', verbose_name='Country'),
        ),
    ]
