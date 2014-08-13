from django.contrib import admin
from forum import models

class AtMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'text', 'type', 'create_time')
    pass

admin.site.register(models.AtMessage, AtMessageAdmin)

class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'point','create_time')
    pass

admin.site.register(models.UserInfo, UserInfoAdmin)

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name','create_time')
    pass

admin.site.register(models.Board, BoardAdmin)

class ReplyInline(admin.TabularInline):
    model = models.Reply

class ThreadAdmin(admin.ModelAdmin):
    inlines = [ReplyInline,]
    search_fields=['title'] 
    list_display = ('id', 'content', 'create_time', 'user')
    pass

admin.site.register(models.Thread, ThreadAdmin)

class ReplyAdmin(admin.ModelAdmin):
    search_fields=['content'] 
    list_display = ('content', 'create_time', 'user')
    pass

admin.site.register(models.Reply, ReplyAdmin)

