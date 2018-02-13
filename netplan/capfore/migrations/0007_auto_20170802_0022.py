# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-02 00:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('capfore', '0006_auto_20170801_1604'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='snippet',
            name='owner',
        ),
        migrations.AddField(
            model_name='task',
            name='progress',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
        migrations.AddField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[('DONE', 'DONE'), ('DOING', 'DOING')], default='python', max_length=100),
        ),
        migrations.AlterField(
            model_name='cityattribute',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city', to='capfore.Task'),
        ),
        migrations.AlterField(
            model_name='packagethreshold',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='package', to='capfore.Task'),
        ),
        migrations.AlterField(
            model_name='sceneattribute',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='scene', to='capfore.Task'),
        ),
        migrations.DeleteModel(
            name='Snippet',
        ),
    ]
