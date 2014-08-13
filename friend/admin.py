from django.contrib import admin
from friend import models

class DocumentAdmin(admin.ModelAdmin):
    list_display = ('name','text', 'create_time')
    pass

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','create_time')
    pass

class CommentAdmin(admin.ModelAdmin):
    list_display = ('text', 'create_time')
    pass

class BigpictureAdmin(admin.ModelAdmin):
    list_display = ('link', 'create_time')
    pass

admin.site.register(models.Bigpicture, BigpictureAdmin)
admin.site.register(models.Document, DocumentAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Comment, CommentAdmin)

