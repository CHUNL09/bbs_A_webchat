from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from ckeditor.fields import RichTextField
import datetime
# Create your models here.

class Article(models.Model):
    title=models.CharField(max_length=255)
    brief=models.CharField(null=True,blank=True,max_length=255)
    category=models.ForeignKey('Category')
    content=RichTextField(u"文章内容")
    author=models.ForeignKey('UserProfile')
    pub_date=models.DateTimeField(blank=True,null=True)
    last_modify_date=models.DateTimeField(auto_now=True)
    status_choices=(('draft',u'草稿'),
                    ('published',u'已发布'),
                    ('offline',u'下线'))
    status=models.CharField(choices=status_choices,default='published',max_length=32)
    priority=models.IntegerField(u"优先级",default=0)
    tag_img=models.ImageField(u"文章标题图片",upload_to='statics/pic')

    def __str__(self):
        return self.title

    def clean(self):
        if self.status=='draft' and self.pub_date is not None:
            raise ValidationError('Draft can not have a publish date')
        if self.status=='published' and self.pub_date is None:
            self.pub_date=datetime.date.today()


class Comment(models.Model):
    article=models.ForeignKey('Article')
    parent_comment=models.ForeignKey('self',related_name='children',null=True,blank=True)
    comment_choices=((1,u'评论'),
                     (2,u'点赞'))
    comment_type=models.IntegerField(choices=comment_choices,default=1)
    user=models.ForeignKey('UserProfile')
    comment=models.TextField(blank=True,null=True)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s(%s)" %(self.article,self.comment)
    def clean(self):
        if self.comment_type==1 and len(self.comment)==0:
            raise ValidationError(u'评论内容不能为空')


class Category(models.Model):
    name=models.CharField(max_length=128,unique=True)
    brief=models.CharField(null=True,blank=True,max_length=255)
    top_display=models.BooleanField(default=False)
    priority=models.IntegerField(default=0)
    manager=models.ManyToManyField('UserProfile')

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user=models.OneToOneField(User)
    name=models.CharField(max_length=32)
    signature=models.CharField(max_length=255,blank=True,null=True)
    head_img=models.ImageField(height_field=150,width_field=150,blank=True,null=True)

    #for web chat
    friends=models.ManyToManyField('self',related_name='my_friends')
    def __str__(self):
        return self.name

