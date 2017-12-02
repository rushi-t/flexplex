# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-20 21:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hoarder', '0005_auto_20170724_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoarding',
            name='last_heartbeat',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 20, 21, 57, 59, 684772)),
        ),
        migrations.AlterField(
            model_name='hoarding',
            name='last_update',
            field=models.DateTimeField(default=datetime.datetime(2017, 8, 20, 21, 57, 59, 684724)),
        ),
        migrations.AlterField(
            model_name='hoarding',
            name='start_time',
            field=models.TimeField(default='08:00 AM'),
        ),
        migrations.AlterField(
            model_name='hoarding',
            name='stop_time',
            field=models.TimeField(default='12:00 PM'),
        ),
    ]