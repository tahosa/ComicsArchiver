# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.TextField(unique=True)),
                ('description', models.TextField()),
                ('folder', models.TextField()),
                ('next_regex', models.TextField()),
                ('comic_regex', models.TextField()),
                ('notes_regex', models.TextField()),
                ('alt_text', models.IntegerField(default=0)),
                ('base_url', models.TextField()),
                ('start_url', models.TextField()),
                ('last_url', models.TextField()),
                ('active', models.IntegerField(default=1)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num', models.IntegerField()),
                ('filename', models.TextField()),
                ('alt_text', models.TextField()),
                ('annotation', models.TextField()),
                ('comic', models.ForeignKey(to='comics.Comic')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='file',
            unique_together=set([('comic', 'filename'), ('comic', 'num')]),
        ),
    ]
