from django.contrib import admin
from .models import Best,Article,Category,Comment,UserProfile
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):

    #将输入栏分块，每个栏也可以定义自己的格式。
    # fieldsets = (
    #     ['Content',
    #      {'fields': ('introdution', 'content'),}],
    # )

    list_display = ('title', 'author_name', 'publish_time')   #自定义页面的显示，比如在列表中显示更多的栏目
    list_filter = ['publish_time']            #按发布时间筛选
    search_fields = ['title']                 #按标题搜索文章

admin.site.register(Article,ArticleAdmin)     #  admin 界面管理文章的数据模型
admin.site.register(Best)                     #  管理精选的数据模型
admin.site.register(Category)                 #  管理分类的数据模型
admin.site.register(Comment)                  #  管理评论的数据模型
admin.site.register(UserProfile)              #  管理用户的数据模型