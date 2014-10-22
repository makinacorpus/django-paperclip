# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration

from paperclip import app_settings


FILETYPE_MODEL = app_settings['FILETYPE_MODEL']


class Migration(SchemaMigration):

    def forwards(self, orm):
        if FILETYPE_MODEL == 'FileType':
            # Adding model 'FileType'
            db.create_table(u'paperclip_filetype', (
                (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
                ('type', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ))
            db.send_create_signal(u'paperclip', ['FileType'])

        # Adding model 'Attachment'
        db.create_table('fl_t_fichier', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['contenttypes.ContentType'])),
            ('object_id', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('attachment_file', self.gf('django.db.models.fields.files.FileField')(max_length=512)),
            ('filetype', self.gf('django.db.models.fields.related.ForeignKey')(to=orm[FILETYPE_MODEL])),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='created_attachments', to=orm['auth.User'])),
            ('author', self.gf('django.db.models.fields.CharField')(default='', max_length=128, db_column='auteur', blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default='', max_length=128, db_column='titre', blank=True)),
            ('legend', self.gf('django.db.models.fields.CharField')(default='', max_length=128, db_column='legende', blank=True)),
            ('date_insert', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('date_update', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'paperclip', ['Attachment'])


    def backwards(self, orm):
        # Deleting model 'FileType'
        db.delete_table(u'paperclip_filetype')

        # Deleting model 'Attachment'
        db.delete_table('fl_t_fichier')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'authent.structure': {
            'Meta': {'ordering': "['name']", 'object_name': 'Structure'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'paperclip.attachment': {
            'Meta': {'ordering': "['-date_insert']", 'object_name': 'Attachment', 'db_table': "'fl_t_fichier'"},
            'attachment_file': ('django.db.models.fields.files.FileField', [], {'max_length': '512'}),
            'author': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'db_column': "'auteur'", 'blank': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created_attachments'", 'to': u"orm['auth.User']"}),
            'date_insert': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'filetype': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['common.FileType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'legend': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'db_column': "'legende'", 'blank': 'True'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128', 'db_column': "'titre'", 'blank': 'True'})
        },
        u'paperclip.filetype': {
            'Meta': {'ordering': "['type']", 'object_name': 'FileType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        }
    }

    complete_apps = ['paperclip']
