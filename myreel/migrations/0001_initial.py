# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AbridgedCast',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AbridgedDirectors',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Director',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('genre', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Links',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('self', models.CharField(max_length=256)),
                ('cast', models.CharField(max_length=256)),
                ('clips', models.CharField(max_length=256)),
                ('reviews', models.CharField(max_length=256)),
                ('similar', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rt_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=256)),
                ('year', models.PositiveIntegerField()),
                ('mpaa_rating', models.CharField(max_length=256)),
                ('runtime', models.PositiveIntegerField()),
                ('critics_consensus', models.CharField(max_length=256)),
                ('release_dates', models.CharField(max_length=256)),
                ('synopsis', models.TextField()),
                ('studio', models.CharField(max_length=256)),
                ('genres', models.ManyToManyField(to='myreel.Genre')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Posters',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('thumbnail', models.CharField(max_length=256)),
                ('original', models.CharField(max_length=256)),
                ('movie', models.ForeignKey(to='myreel.Movie')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('critics_rating', models.CharField(max_length=256)),
                ('critics_score', models.SmallIntegerField()),
                ('audience_rating', models.CharField(max_length=256)),
                ('audience_score', models.SmallIntegerField()),
                ('movie', models.ForeignKey(to='myreel.Movie')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('studio', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='links',
            name='movie',
            field=models.ForeignKey(to='myreel.Movie'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abridgeddirectors',
            name='directors',
            field=models.ManyToManyField(to='myreel.Director'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abridgeddirectors',
            name='movie',
            field=models.ForeignKey(to='myreel.Movie'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abridgedcast',
            name='actors',
            field=models.ManyToManyField(to='myreel.Actor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='abridgedcast',
            name='movie',
            field=models.ForeignKey(to='myreel.Movie'),
            preserve_default=True,
        ),
    ]
