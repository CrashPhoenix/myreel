# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myreel', '0005_userprofile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movie',
            old_name='release_dates',
            new_name='release_date',
        ),
    ]
