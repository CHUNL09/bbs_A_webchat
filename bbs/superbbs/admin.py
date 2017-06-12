from django.contrib import admin
from superbbs import models
# Register your models here.

class CommentAdmin(admin.ModelAdmin):
    list_display = ('article','parent_comment','comment_type','comment','user')
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','top_display','priority')
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category','author','status','pub_date','priority')


admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.Comment,CommentAdmin)
admin.site.register(models.UserProfile)
admin.site.register(models.Category,CategoryAdmin)