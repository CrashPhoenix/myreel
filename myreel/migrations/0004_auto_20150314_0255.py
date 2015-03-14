# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myreel', '0003_auto_20150309_0549'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='studios',
            field=models.ManyToManyField(to='myreel.Studio', blank=True),
            preserve_default=True,
        ),
    ]
