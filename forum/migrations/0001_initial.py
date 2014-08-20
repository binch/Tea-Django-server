# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Like'
        db.create_table('forum_like', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='likes', to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='forum', max_length=255)),
            ('from_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('forum', ['Like'])

        # Adding model 'Favor'
        db.create_table('forum_favor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='favors', to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='forum', max_length=255)),
            ('from_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('forum', ['Favor'])

        # Adding model 'AtMessage'
        db.create_table('forum_atmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='atmessages', to=orm['auth.User'])),
            ('type', self.gf('django.db.models.fields.CharField')(default='forum', max_length=255)),
            ('read', self.gf('django.db.models.fields.CharField')(default='unread', max_length=255)),
            ('text', self.gf('django.db.models.fields.CharField')(default='', max_length=2550)),
            ('from_id', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('forum', ['AtMessage'])

        # Adding model 'UserInfo'
        db.create_table('forum_userinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('nickname', self.gf('django.db.models.fields.CharField')(default='', max_length=2550, blank=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(default='', max_length=2550, blank=True)),
            ('deviceid', self.gf('django.db.models.fields.CharField')(default='', max_length=2550, blank=True)),
            ('thumb', self.gf('django.db.models.fields.CharField')(default='', max_length=2550, blank=True)),
            ('point', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('forum', ['UserInfo'])

        # Adding model 'Board'
        db.create_table('forum_board', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('desc', self.gf('django.db.models.fields.TextField')(default='test')),
            ('index3', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('forum', ['Board'])

        # Adding model 'Thread'
        db.create_table('forum_thread', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('images_1', self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(related_name='threads', to=orm['forum.Board'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='threads', to=orm['auth.User'])),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('last_reply', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
        ))
        db.send_create_signal('forum', ['Thread'])

        # Adding model 'ThreadImage'
        db.create_table('forum_threadimage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(related_name='images', to=orm['forum.Thread'])),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('forum', ['ThreadImage'])

        # Adding model 'Reply'
        db.create_table('forum_reply', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=2550)),
            ('images_1', self.gf('django.db.models.fields.CharField')(default='', max_length=2550, blank=True)),
            ('thread', self.gf('django.db.models.fields.related.ForeignKey')(related_name='replys', to=orm['forum.Thread'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='replys', to=orm['auth.User'])),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('forum', ['Reply'])

        # Adding model 'UserThreadCount'
        db.create_table('forum_userthreadcount', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['forum.Board'])),
            ('readed_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('forum', ['UserThreadCount'])


    def backwards(self, orm):
        
        # Deleting model 'Like'
        db.delete_table('forum_like')

        # Deleting model 'Favor'
        db.delete_table('forum_favor')

        # Deleting model 'AtMessage'
        db.delete_table('forum_atmessage')

        # Deleting model 'UserInfo'
        db.delete_table('forum_userinfo')

        # Deleting model 'Board'
        db.delete_table('forum_board')

        # Deleting model 'Thread'
        db.delete_table('forum_thread')

        # Deleting model 'ThreadImage'
        db.delete_table('forum_threadimage')

        # Deleting model 'Reply'
        db.delete_table('forum_reply')

        # Deleting model 'UserThreadCount'
        db.delete_table('forum_userthreadcount')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'forum.atmessage': {
            'Meta': {'object_name': 'AtMessage'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'read': ('django.db.models.fields.CharField', [], {'default': "'unread'", 'max_length': '255'}),
            'text': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2550'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'forum'", 'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'atmessages'", 'to': "orm['auth.User']"})
        },
        'forum.board': {
            'Meta': {'object_name': 'Board'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {'default': "'test'"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index3': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'forum.favor': {
            'Meta': {'object_name': 'Favor'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'forum'", 'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'favors'", 'to': "orm['auth.User']"})
        },
        'forum.like': {
            'Meta': {'object_name': 'Like'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'from_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'forum'", 'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'default': '1', 'related_name': "'likes'", 'to': "orm['auth.User']"})
        },
        'forum.reply': {
            'Meta': {'object_name': 'Reply'},
            'content': ('django.db.models.fields.CharField', [], {'max_length': '2550'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2550', 'blank': 'True'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replys'", 'to': "orm['forum.Thread']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'replys'", 'to': "orm['auth.User']"})
        },
        'forum.thread': {
            'Meta': {'object_name': 'Thread'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'threads'", 'to': "orm['forum.Board']"}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images_1': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'last_reply': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'threads'", 'to': "orm['auth.User']"})
        },
        'forum.threadimage': {
            'Meta': {'object_name': 'ThreadImage'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'thread': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'images'", 'to': "orm['forum.Thread']"})
        },
        'forum.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2550', 'blank': 'True'}),
            'deviceid': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2550', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nickname': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2550', 'blank': 'True'}),
            'point': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'thumb': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2550', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'forum.userthreadcount': {
            'Meta': {'object_name': 'UserThreadCount'},
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['forum.Board']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'readed_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['forum']
