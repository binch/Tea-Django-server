from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class QACategory(models.Model):
    name = models.CharField(max_length=2550)
    create_time = models.DateTimeField(auto_now_add=True)
    def __unicode__(self):
        return self.name

class Question(models.Model):
    ended = models.BooleanField(default=False)
    title = models.CharField(max_length=2550)
    content = models.TextField()
    images_1 = models.CharField(max_length=2550, default='')
    create_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name='questions')
    category = models.ForeignKey(QACategory, related_name='questions')
    def __unicode__(self):
        return self.title

class Answer(models.Model):
    content = models.TextField()
    accepted = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    images_1 = models.CharField(max_length=2550, default='')
    question = models.ForeignKey(Question, related_name='answers')
    user = models.ForeignKey(User, related_name='answers')
    def __unicode__(self):
        return str(self.id)



