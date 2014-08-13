from django.contrib import admin
from shop import models

class ShopCategoryInline(admin.TabularInline):
    model = models.ShopCategory

class OrderItemInline(admin.TabularInline):
    model = models.OrderItem

class ShopAdmin(admin.ModelAdmin):
    inlines = [ShopCategoryInline,]
    list_display = ('title','create_time')
    pass

admin.site.register(models.Shop, ShopAdmin)

class ShopCategoryAdmin(admin.ModelAdmin):
    list_display = ('name','create_time')
    pass

admin.site.register(models.ShopCategory, ShopCategoryAdmin)

class PromotionAdmin(admin.ModelAdmin):
    list_display = ('id', 'create_time')
    pass

admin.site.register(models.Promotion, PromotionAdmin)

class ItemCommentAdmin(admin.ModelAdmin):
    search_fields=['title'] 
    list_display = ('title', 'create_time')
    pass

admin.site.register(models.ItemComment, ItemCommentAdmin)

class CommentInline(admin.TabularInline):
    model = models.ItemComment

class ItemAdmin(admin.ModelAdmin):
    inlines = [CommentInline,]
    search_fields=['title'] 
    list_display = ('id', 'title', 'create_time')
    pass

admin.site.register(models.Item, ItemAdmin)

class OrderAdmin(admin.ModelAdmin):
    search_fields=['owner'] 
    list_display = ('id', 'create_time')
    inlines = [OrderItemInline,]
    pass

admin.site.register(models.Order, OrderAdmin)


