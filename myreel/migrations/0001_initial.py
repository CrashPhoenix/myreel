# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Backdrop',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('w300', models.CharField(max_length=256)),
                ('w780', models.CharField(max_length=256)),
                ('w1280', models.CharField(max_length=256)),
                ('original', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Character',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('character', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CrewMember',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tmdb_id', models.PositiveIntegerField()),
                ('genre', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('w45', models.CharField(max_length=256)),
                ('w92', models.CharField(max_length=256)),
                ('w154', models.CharField(max_length=256)),
                ('w185', models.CharField(max_length=256)),
                ('w300', models.CharField(max_length=256)),
                ('w500', models.CharField(max_length=256)),
                ('original', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tmdb_id', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=256)),
                ('overview', models.TextField()),
                ('release_date', models.DateTimeField()),
                ('imdb_id', models.PositiveIntegerField()),
                ('popularity', models.FloatField()),
                ('userrating', models.FloatField()),
                ('votes', models.PositiveIntegerField()),
                ('adult', models.BooleanField()),
                ('cast', models.ManyToManyField(to='myreel.Character')),
                ('crew', models.ManyToManyField(to='myreel.CrewMember')),
                ('genres', models.ManyToManyField(to='myreel.Genre')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tmdb_id', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=256)),
                ('biography', models.TextField()),
                ('dayofbirth', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Poster',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('w92', models.CharField(max_length=256)),
                ('w154', models.CharField(max_length=256)),
                ('w185', models.CharField(max_length=256)),
                ('w342', models.CharField(max_length=256)),
                ('w500', models.CharField(max_length=256)),
                ('w780', models.CharField(max_length=256)),
                ('original', models.CharField(max_length=256)),
                ('movie', models.ForeignKey(to='myreel.Movie')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('w45', models.CharField(max_length=256)),
                ('w185', models.CharField(max_length=256)),
                ('h632', models.CharField(max_length=256)),
                ('original', models.CharField(max_length=256)),
                ('person', models.ForeignKey(to='myreel.Person')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Reel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('movies', models.ManyToManyField(to='myreel.Movie')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tmdb_id', models.PositiveIntegerField()),
                ('studio', models.CharField(max_length=256)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('reels', models.ManyToManyField(to='myreel.Reel')),
                ('user', models.OneToOneField(related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='movie',
            name='studios',
            field=models.ManyToManyField(to='myreel.Studio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='logo',
            name='studio',
            field=models.ForeignKey(to='myreel.Studio'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='crewmember',
            name='person',
            field=models.ForeignKey(to='myreel.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='character',
            name='person',
            field=models.ForeignKey(to='myreel.Person'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='backdrop',
            name='movie',
            field=models.ForeignKey(to='myreel.Movie'),
            preserve_default=True,
        ),
    ]
