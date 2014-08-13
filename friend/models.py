from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name

class Document(models.Model):
    '''A Document is a blog post or wiki entry with some text content'''
    category = models.ForeignKey(Category, related_name='documents')
    name = models.CharField(max_length=255)
    pic_url = models.CharField(max_length=255, default='')
    text = models.TextField()
    summary = models.TextField(default='')
    create_time = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name

class Comment(models.Model):
    '''A Comment is some text about a given Document'''
    document = models.ForeignKey(Document, related_name='comments')
    text = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

class Bigpicture(models.Model):
    '''A Comment is some text about a given Document'''
    pic_url = models.CharField(max_length=2550, default='')
    link = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)

