# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myreel', '0006_auto_20141227_0033'),
    ]

    operations = [
        migrations.AddField(
            model_name='posters',
            name='detailed',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='posters',
            name='profile',
            field=models.CharField(default=None, max_length=256),
            preserve_default=False,
        ),
    ]
