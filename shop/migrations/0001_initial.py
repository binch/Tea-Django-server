# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Shop'
        db.create_table('shop_shop', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('desc', self.gf('django.db.models.fields.TextField')()),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='shops', to=orm['auth.User'])),
        ))
        db.send_create_signal('shop', ['Shop'])

        # Adding model 'Order'
        db.create_table('shop_order', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('addr', self.gf('django.db.models.fields.CharField')(default='', max_length=2550)),
            ('phone', self.gf('django.db.models.fields.CharField')(default='', max_length=2550)),
            ('contact', self.gf('django.db.models.fields.CharField')(default='', max_length=2550)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orders', to=orm['auth.User'])),
            ('total', self.gf('django.db.models.fields.FloatField')()),
            ('status', self.gf('django.db.models.fields.CharField')(default='new', max_length=255)),
            ('pay', self.gf('django.db.models.fields.CharField')(default='cod', max_length=255)),
        ))
        db.send_create_signal('shop', ['Order'])

        # Adding model 'ShopCategory'
        db.create_table('shop_shopcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('index3', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cats', to=orm['shop.Shop'])),
        ))
        db.send_create_signal('shop', ['ShopCategory'])

        # Adding model 'Item'
        db.create_table('shop_item', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('sold', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('images', self.gf('django.db.models.fields.TextField')(default='')),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('category', self.gf('django.db.models.fields.related.ForeignKey')(related_name='cats', to=orm['shop.ShopCategory'])),
            ('price', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal('shop', ['Item'])

        # Adding model 'ItemComment'
        db.create_table('shop_itemcomment', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(default='binch', related_name='itemcomments', to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=2550)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('images', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('ziwei', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('xiangqi', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('naipao', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('yexing', self.gf('django.db.models.fields.IntegerField')(default=3)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='comments', to=orm['shop.Item'])),
        ))
        db.send_create_signal('shop', ['ItemComment'])

        # Adding model 'OrderItem'
        db.create_table('shop_orderitem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='orderitems', to=orm['shop.Item'])),
            ('count', self.gf('django.db.models.fields.IntegerField')()),
            ('order', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['shop.Order'])),
        ))
        db.send_create_signal('shop', ['OrderItem'])

        # Adding model 'Promotion'
        db.create_table('shop_promotion', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='promotions', to=orm['auth.User'])),
            ('shop', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='promotions', to=orm['shop.Shop'])),
            ('item', self.gf('django.db.models.fields.related.ForeignKey')(default=0, related_name='promotions', to=orm['shop.Item'])),
            ('image_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('shop', ['Promotion'])


    def backwards(self, orm):
        
        # Deleting model 'Shop'
        db.delete_table('shop_shop')

        # Deleting model 'Order'
        db.delete_table('shop_order')

        # Deleting model 'ShopCategory'
        db.delete_table('shop_shopcategory')

        # Deleting model 'Item'
        db.delete_table('shop_item')

        # Deleting model 'ItemComment'
        db.delete_table('shop_itemcomment')

        # Deleting model 'OrderItem'
        db.delete_table('shop_orderitem')

        # Deleting model 'Promotion'
        db.delete_table('shop_promotion')


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
        'shop.item': {
            'Meta': {'object_name': 'Item'},
            'category': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cats'", 'to': "orm['shop.ShopCategory']"}),
            'content': ('django.db.models.fields.TextField', [], {}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'sold': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'shop.itemcomment': {
            'Meta': {'object_name': 'ItemComment'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'images': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'comments'", 'to': "orm['shop.Item']"}),
            'naipao': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'default': "'binch'", 'related_name': "'itemcomments'", 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2550'}),
            'xiangqi': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'yexing': ('django.db.models.fields.IntegerField', [], {'default': '3'}),
            'ziwei': ('django.db.models.fields.IntegerField', [], {'default': '3'})
        },
        'shop.order': {
            'Meta': {'object_name': 'Order'},
            'addr': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2550'}),
            'contact': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2550'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orders'", 'to': "orm['auth.User']"}),
            'pay': ('django.db.models.fields.CharField', [], {'default': "'cod'", 'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '2550'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '255'}),
            'total': ('django.db.models.fields.FloatField', [], {})
        },
        'shop.orderitem': {
            'Meta': {'object_name': 'OrderItem'},
            'count': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'orderitems'", 'to': "orm['shop.Item']"}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['shop.Order']"})
        },
        'shop.promotion': {
            'Meta': {'object_name': 'Promotion'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'item': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'promotions'", 'to': "orm['shop.Item']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'promotions'", 'to': "orm['auth.User']"}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'default': '0', 'related_name': "'promotions'", 'to': "orm['shop.Shop']"})
        },
        'shop.shop': {
            'Meta': {'object_name': 'Shop'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'shops'", 'to': "orm['auth.User']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'shop.shopcategory': {
            'Meta': {'object_name': 'ShopCategory'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index3': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'shop': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'cats'", 'to': "orm['shop.Shop']"})
        }
    }

    complete_apps = ['shop']
