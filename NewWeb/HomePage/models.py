from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

# 分类表
class Category(models.Model):
    name=models.CharField(max_length=50,null=False)     #每个字段都是 Field 类的实例,字符字段被表示为 CharField

    def __str__(self):          # 显示分类
        return self.name

#文章表
class Article(models.Model):
    title=models.CharField(max_length=100,null=False)     #标题,max_length 参数用来定义数据库结构，也用于验证数据
    introdution=models.CharField(max_length=300)       #导语
    image = models.FileField(upload_to='article_image')  # 文章配图
    author_name = models.CharField(max_length=100, null=False)  # 作者名字
    publish_time = models.DateTimeField(null=False, default=timezone.now)  # 发布时间,日期时间字段被表示为 DateTimeField
    source_link = models.CharField(max_length=200)  # 原文链接
    category = models.ForeignKey(Category, related_name='cate',on_delete=models.CASCADE) # 连接分类表的外键,多对一关系,反向名称related_name，用来从被关联字段指向关联字段
    # on_delete当一个model对象的ForeignKey关联的对象被删除时，默认情况下此对象也会一起被级联删除的。CASCADE: 默认值，model对象会和ForeignKey关联对象一起被删除
    content = models.TextField(null=False)  # 内容

    def __str__(self):
        return self.title

# 精选文章
class Best(models.Model):
    select_article = models.ForeignKey(Article, related_name='select_article',on_delete=models.CASCADE)  # 被精选的文章
    Select_Reason = (
        ('今日新闻', '今日新闻'),
        ('热点要闻', '热点要闻'),
        ('推荐阅读', '推荐阅读')
    )
    select_reason = models.CharField(choices=Select_Reason, max_length=60, null=False)  # 精选的理由

    def __str__(self):
        return self.select_reason + '-' + self.select_article.title

#用户信息表
class UserProfile(models.Model):
    belong_to = models.OneToOneField(to=User, related_name="profile",on_delete=models.CASCADE)  # 所属用户,一对一
    avatar = models.FileField(upload_to='avatar')  # 用户头像

    def __str__(self):
        return self.belong_to.username

# 评论表
class Comment(models.Model):
    belong_article = models.ForeignKey(Article, related_name='article',on_delete=models.CASCADE)  # 评论所属的文章
    belong_user = models.ForeignKey(User, related_name='user',on_delete=models.CASCADE)  # 评论者
    words = models.CharField(max_length=200, null=False)  # 评论内容
    created = models.DateTimeField(null=False, default=timezone.now)  # 评论时间

    def __str__(self):
        return self.belong_user.username + ': ' + self.words

