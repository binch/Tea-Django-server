# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Bigpicture'
        db.create_table('friend_bigpicture', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pic_url', self.gf('django.db.models.fields.CharField')(default='', max_length=2550)),
            ('link', self.gf('django.db.models.fields.TextField')()),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('friend', ['Bigpicture'])


    def backwards(self, orm):
        
        # Deleting model 'Bigpicture'
        db.delete_table('friend_bigpicture')


    models = {
        'friend.bigpicture': {
            'Meta': {'object_name': 'Bigpicture'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.TextField', [], {}),
            'pic_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2550'})
        },
        'friend.category': {
            'Meta': {'object_name': 'Category'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'friend.comment': {
            'Meta': {'object_name': 'Comment'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'document': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['friend.Document']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'friend.document': {
            'Meta': {'object_name': 'Document'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'documents'", 'to': "orm['friend.Category']"}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'pic_url': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'summary': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'text': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['friend']
