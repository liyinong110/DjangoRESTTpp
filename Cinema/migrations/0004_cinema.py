# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-12 16:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Cinema', '0003_cinemamovieorder_is_delete'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cinema',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('c_name', models.CharField(max_length=64)),
                ('c_address', models.CharField(max_length=128)),
                ('c_phone', models.CharField(max_length=32)),
                ('is_active', models.BooleanField(default=False)),
                ('c_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Cinema.CinemaUser')),
            ],
        ),
    ]
