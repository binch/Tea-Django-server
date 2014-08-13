from django.contrib import admin
from forum import models
from qa import models

class QACategoryAdmin(admin.ModelAdmin):
    list_display = ('name','create_time')
    pass

admin.site.register(models.QACategory, QACategoryAdmin)

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('ended', 'title','create_time')
    pass

admin.site.register(models.Question, QuestionAdmin)

class AnswerAdmin(admin.ModelAdmin):
    search_fields=['title'] 
    list_display = ('content', 'accepted', 'create_time', 'user')
    pass

admin.site.register(models.Answer, AnswerAdmin)


