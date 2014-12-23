# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myreel', '0002_reel_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='myreels',
        ),
        migrations.AddField(
            model_name='reel',
            name='user',
            field=models.ForeignKey(to='myreel.UserProfile', null=True),
            preserve_default=True,
        ),
    ]
