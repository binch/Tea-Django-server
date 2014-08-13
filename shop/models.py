# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Shop(models.Model):
    title = models.CharField(max_length=255)
    desc = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='shops')
    def __unicode__(self):
        return self.title

class Order(models.Model):
    addr = models.CharField(max_length=2550, default='')
    phone = models.CharField(max_length=2550, default='')
    contact = models.CharField(max_length=2550, default='')
    create_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='orders')
    total = models.FloatField()
    STATUSES = (
        (u'new', '新建'),
        (u'paid', '已付款'),
        (u'shipped', '已发货'),
        (u'completed', '已完成'),
        (u'cancelled', '已取消'),
    )
    PAYS = (
        (u'alipay', u'支付宝'),
         (u'cod', u'货到付款'),
        )
    status = models.CharField(max_length=255, choices=STATUSES, default='new')
    pay = models.CharField(max_length=255, choices=PAYS, default='cod')
    def __unicode__(self):
        return str(self.id)

class ShopCategory(models.Model):
    name = models.CharField(max_length=255)
    index3 = models.IntegerField(default=10)
    create_time = models.DateTimeField(auto_now_add=True)
    shop = models.ForeignKey(Shop, related_name='cats')
    def __unicode__(self):
        return self.shop.title + '|' + self.name

class Item(models.Model):
    title = models.CharField(max_length=255)
    sold = models.IntegerField(default=0)
    content = models.TextField()
    images = models.TextField(default='')
    create_time = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(ShopCategory, related_name='cats')
    price = models.FloatField()
    def __unicode__(self):
        return self.title


class ItemComment(models.Model):
    owner = models.ForeignKey(User, related_name='itemcomments')
    title = models.CharField(max_length=2550)
    content = models.TextField()
    images = models.TextField(default='', blank=True)
    create_time = models.DateTimeField(auto_now_add=True)
    ziwei = models.IntegerField(default=3)
    xiangqi = models.IntegerField(default=3)
    naipao = models.IntegerField(default=3)
    yexing = models.IntegerField(default=3)
    item = models.ForeignKey(Item, related_name='comments')

    def __unicode__(self):
        return self.title

class OrderItem(models.Model):
    item = models.ForeignKey(Item, related_name='orderitems')
    count = models.IntegerField()
    order = models.ForeignKey(Order, related_name='items')

class Promotion(models.Model):
    create_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, related_name='promotions')
    shop = models.ForeignKey(Shop, related_name='promotions', default=0)
    item = models.ForeignKey(Item, related_name='promotions', default=0)
    image_name = models.CharField(max_length=255)
    def __unicode__(self):
        return str(self.id)


