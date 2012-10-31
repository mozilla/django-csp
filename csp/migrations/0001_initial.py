# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table('csp_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=40)),
        ))
        db.send_create_signal('csp', ['Group'])

        # Adding model 'Report'
        db.create_table('csp_report', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['csp.Group'], null=True, blank=True)),
            ('document_uri', self.gf('django.db.models.fields.URLField')(max_length=400, db_index=True)),
            ('blocked_uri', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=400, null=True, blank=True)),
            ('referrer', self.gf('django.db.models.fields.URLField')(max_length=400, null=True, blank=True)),
            ('violated_directive', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=1000, null=True, blank=True)),
            ('original_policy', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('source_file', self.gf('django.db.models.fields.CharField')(max_length=400, null=True, blank=True)),
            ('line_number', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('script_sample', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('reported', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, db_index=True)),
        ))
        db.send_create_signal('csp', ['Report'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table('csp_group')

        # Deleting model 'Report'
        db.delete_table('csp_report')


    models = {
        'csp.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '40'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'csp.report': {
            'Meta': {'object_name': 'Report'},
            'blocked_uri': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'document_uri': ('django.db.models.fields.URLField', [], {'max_length': '400', 'db_index': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['csp.Group']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'line_number': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'original_policy': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'referrer': ('django.db.models.fields.URLField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'reported': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'db_index': 'True'}),
            'script_sample': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'source_file': ('django.db.models.fields.CharField', [], {'max_length': '400', 'null': 'True', 'blank': 'True'}),
            'violated_directive': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '1000', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['csp']