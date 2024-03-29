# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-25 14:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cmdb', '0020_workstation_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='Printer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Software Name')),
                ('description', models.CharField(max_length=200, verbose_name='Description')),
            ],
            options={
                'ordering': ('name',),
                'verbose_name': 'Printer',
                'verbose_name_plural': 'Printers',
            },
        ),
        migrations.AlterField(
            model_name='software',
            name='workstations',
            field=models.ManyToManyField(to='cmdb.Workstation', verbose_name='Computer Name'),
        ),
        migrations.AlterField(
            model_name='workstation',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.ComputerCategory', verbose_name='Computer Category'),
        ),
        migrations.AlterField(
            model_name='workstation',
            name='location',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='cmdb.Location', verbose_name='Office'),
        ),
    ]
