# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myreel', '0004_auto_20150314_0255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='studios',
            field=models.ManyToManyField(to='myreel.Studio'),
            preserve_default=True,
        ),
    ]
