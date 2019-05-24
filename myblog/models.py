from django.db import models

from django.contrib.auth.models import User
# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse  #反向解析
from read_statistics.models import ReadNumExpendMethod,ReadDetail
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit
# Create your models here.



class BlogType(models.Model):
    type_name = models.CharField(max_length=15)  #类型标题

    def __str__(self):  #将一个类的示例转换为字符串的形式
        return self.type_name

class Blog(models.Model,ReadNumExpendMethod):
    title = models.CharField(max_length=50)  #文章标题
    blog_type = models.ForeignKey(BlogType,on_delete=models.CASCADE ,related_name="blog_blog")
    #外键管理
    content = RichTextUploadingField()  #内容，使用长文本字段
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    read_details = GenericRelation(ReadDetail)
    # read_num = models.IntegerField(default=0)  #阅读计数字段
    created_time = models.DateTimeField(auto_now_add = True,)  #auto_now_add 首次创建对象时自动将字段设置为现在
    last_update_time = models.DateTimeField(auto_now=True,) #auto_now  用于创建和修改字段
    #给文章博客添加封面
    avator =ProcessedImageField(
        #数据库中保存的实际上是封面的对应地址
        upload_to='avator/',
        processors=[ResizeToFit(width=140)],
        format='JPEG',
        options={'quality': 100},
        #设置默认的封面
        default='/avator/default.jpg',
    )
    def get_url(self):
        return reverse('myblog:blog_detail',kwargs={'blog_pk':self.pk})
    
    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<Blog: %s>"%self.title


    class Meta:
        ordering =['-created_time']  #


    

