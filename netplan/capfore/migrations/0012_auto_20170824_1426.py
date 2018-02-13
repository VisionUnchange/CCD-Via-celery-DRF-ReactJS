# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-24 14:26
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capfore', '0011_auto_20170823_0613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='foredate',
        ),
        migrations.AddField(
            model_name='task',
            name='curdate',
            field=models.DateField(default=datetime.date(2017, 6, 1), verbose_name='当前数据时间点'),
        ),
        migrations.AddField(
            model_name='task',
            name='period',
            field=models.IntegerField(default=1, verbose_name='预测周期'),
        ),
        migrations.AlterField(
            model_name='task',
            name='progress',
            field=models.FloatField(default=0),
        ),
    ]
