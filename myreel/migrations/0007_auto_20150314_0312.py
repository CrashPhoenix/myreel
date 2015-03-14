# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myreel', '0006_auto_20150314_0308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='dayofbirth',
            field=models.DateTimeField(null=True),
            preserve_default=True,
        ),
    ]
