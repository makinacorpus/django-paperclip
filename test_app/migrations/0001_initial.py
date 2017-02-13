# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('paperclip', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestAttachment',
            fields=[
                ('attachment_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='paperclip.Attachment')),
                ('foo', models.CharField(max_length=100)),
            ],
            bases=('paperclip.attachment',),
        ),
        migrations.CreateModel(
            name='TestFiletype',
            fields=[
                ('filetype_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='paperclip.FileType')),
                ('foo', models.CharField(max_length=100)),
            ],
            bases=('paperclip.filetype',),
        ),
        migrations.CreateModel(
            name='TestObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
    ]
