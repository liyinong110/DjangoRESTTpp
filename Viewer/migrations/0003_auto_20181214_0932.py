# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-12-14 09:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Viewer', '0002_viewerorder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewerorder',
            name='v_expire',
            field=models.DateTimeField(default=datetime.datetime(2018, 12, 14, 9, 32, 34, 855134)),
        ),
    ]
