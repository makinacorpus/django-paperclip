# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields
from django.conf import settings
import paperclip.models
import django


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id', models.PositiveIntegerField()),
                ('attachment_file', models.FileField(upload_to=paperclip.models.attachment_upload, max_length=512, verbose_name='File', blank=True)),
                ('attachment_video', embed_video.fields.EmbedVideoField(verbose_name='URL', blank=True)),
                ('author', models.CharField(db_column='author', default='', max_length=128, blank=True, help_text='Original creator', verbose_name='Author')),
                ('title', models.CharField(db_column='title', default='', max_length=128, blank=True, help_text='Renames the file', verbose_name='Filename')),
                ('legend', models.CharField(db_column='legend', default='', max_length=128, blank=True, help_text='Details displayed', verbose_name='Legend')),
                ('starred', models.BooleanField(default=False, help_text='Mark as starred', verbose_name='Starred', db_column='starred')),
                ('date_insert', models.DateTimeField(auto_now_add=True, verbose_name='Insertion date')),
                ('date_update', models.DateTimeField(auto_now=True, verbose_name='Update date')),
                ('foo', models.CharField(max_length=100)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType', on_delete=django.db.models.deletion.CASCADE,)),
                ('creator', models.ForeignKey(related_name='created_attachments', verbose_name='Creator', to=settings.AUTH_USER_MODEL, help_text='User that uploaded', on_delete=django.db.models.deletion.CASCADE,)),
            ],
            options={
                'ordering': ['-date_insert'],
                'abstract': False,
                'verbose_name_plural': 'Attachments',
                'default_permissions': (),
                'verbose_name': 'Attachment',
                'permissions': (('add_attachment', 'Can add attachments'), ('change_attachment', 'Can change attachments'), ('delete_attachment', 'Can delete attachments'), ('read_attachment', 'Can read attachments'), ('delete_attachment_others', "Can delete others' attachments")),
            },
        ),
        migrations.CreateModel(
            name='Filetype',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=128, verbose_name='File type')),
                ('foo', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ['type'],
                'abstract': False,
                'verbose_name': 'File type',
                'verbose_name_plural': 'File types',
            },
        ),
        migrations.CreateModel(
            name='TestObject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='attachment',
            name='filetype',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, verbose_name='File type', to='test_app.Filetype'),
        ),
    ]
