# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RedirectTranslation.redirect_type'
        db.add_column(u'redirects_hvad_redirect_translation', 'redirect_type',
                      self.gf('django.db.models.fields.IntegerField')(default=302),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RedirectTranslation.redirect_type'
        db.delete_column(u'redirects_hvad_redirect_translation', 'redirect_type')


    models = {
        u'redirects_hvad.redirect': {
            'Meta': {'ordering': "('old_path',)", 'unique_together': "(('site', 'old_path'),)", 'object_name': 'Redirect'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'old_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'redirects_hvad_set'", 'to': u"orm['sites.Site']"})
        },
        u'redirects_hvad.redirecttranslation': {
            'Meta': {'unique_together': "[('language_code', 'master')]", 'object_name': 'RedirectTranslation', 'db_table': "u'redirects_hvad_redirect_translation'"},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'db_index': 'True'}),
            'master': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'translations'", 'null': 'True', 'to': u"orm['redirects_hvad.Redirect']"}),
            'new_path': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'redirect_type': ('django.db.models.fields.IntegerField', [], {'default': '301'})
        },
        u'sites.site': {
            'Meta': {'ordering': "('domain',)", 'object_name': 'Site', 'db_table': "'django_site'"},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['redirects_hvad']