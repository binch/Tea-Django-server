# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User

class Like(models.Model):
    TYPES = (
        (u'thread', u'贴子'),
        (u'article', u'文章'),
        (u'item', u'商品'),
        (u'shop', u'商店'),
    )
    user = models.ForeignKey(User, related_name='likes', default=1)
    type = models.CharField(max_length=255, choices=TYPES, default='forum')
    from_id = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.id)

class Favor(models.Model):
    TYPES = (
        (u'thread', u'贴子'),
        (u'article', u'文章'),
        (u'item', u'商品'),
        (u'shop', u'商店'),
    )
    user = models.ForeignKey(User, related_name='favors', default=1)
    type = models.CharField(max_length=255, choices=TYPES, default='forum')
    from_id = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.id)

class AtMessage(models.Model):
    READ = (
        (u'read', u'已读'),
        (u'unread', u'未读'),
    )
    TYPES = (
        (u'forum', u'论坛'),
        (u'qa', u'问答'),
    )
    user = models.ForeignKey(User, related_name='atmessages', default=1)
    type = models.CharField(max_length=255, choices=TYPES, default='forum')
    read_status = models.CharField(max_length=255, choices=READ, default='unread')
    text = models.CharField(max_length=2550, default='')
    from_id = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return str(self.id)

class UserInfo(models.Model):
    user = models.OneToOneField(User)
    create_time = models.DateTimeField(auto_now_add=True)
    nickname = models.CharField(max_length=2550, default='', blank=True)
    user_desc = models.CharField(max_length=2550, default='', blank=True)
    deviceid = models.CharField(max_length=2550, default='', blank=True)
    thumb = models.CharField(max_length=2550, default='', blank=True)
    point = models.IntegerField(default=0)
    def __unicode__(self):
        return self.user.username


# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    board_desc = models.TextField(default='test')
    index3 = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name

class Thread(models.Model):
    title = models.CharField(max_length=255)
    images_1 = models.CharField(max_length=255, default='', blank=True)
    content = models.CharField(max_length=255)
    board = models.ForeignKey(Board, related_name='threads')
    user = models.ForeignKey(User, related_name='threads')
    create_time = models.DateTimeField(auto_now_add=True)
    last_reply = models.DateTimeField(blank=True)

    def __unicode__(self):
        return self.title

class ThreadImage(models.Model):
    thread = models.ForeignKey(Thread, related_name='images')
    image = models.ImageField(upload_to='threadimages')
    create_time = models.DateTimeField(auto_now_add=True)

class Reply(models.Model):
    content = models.CharField(max_length=2550)
    images_1 = models.CharField(max_length=2550, default='', blank=True)
    thread = models.ForeignKey(Thread, related_name='replys')
    user = models.ForeignKey(User, related_name='replys')
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.content

class UserThreadCount(models.Model):
    user = models.ForeignKey(User)
    board = models.ForeignKey(Board)
    readed_count = models.IntegerField(default=0)
