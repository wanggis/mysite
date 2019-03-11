import threading
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.shortcuts import render
# Create your models here.


class SendMail(threading.Thread):
    def __init__(self,subject,text,email,fail_silently=False):
        self.subject = subject
        self.text = text
        self .email  = email
        self.fail_silently = fail_silently
        threading.Thread.__init__(self)

    def run(self):
        send_mail(
            self.subject,
            self.text,
            # 'from@example.com',
            # ['to@example.com'],
            # fail_silently=False,
            # subject,
            # text,
            # '验证码: %s' % code,
            '3463854346@qq.com',
            [self.email],
            fail_silently=self.fail_silently,
            html_message=self.text
        )


class Comment(models.Model):
    #评论对象，不进行设置，所以要用到ContentType
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    # 评论内容
    comment_text = models.TextField()  
    #评论时间
    comment_time = models.DateTimeField(auto_now_add=True)
    #评论人
    user = models.ForeignKey(User,related_name="comments",on_delete=models.CASCADE)   #related_name="comments"！！！！！！！！！！显示关联的
     #关联上一级的评论
    root = models.ForeignKey('self',related_name="root_comment",null=True,on_delete=models.CASCADE)
    parent = models.ForeignKey('self' ,null=True, related_name='parent_comment',on_delete=models.CASCADE)
    #回复谁
    reply_to = models.ForeignKey(User,null=True,related_name="replies",on_delete=models.CASCADE)

    def send_mail(self):
        # 发送右键通知
        if self.parent is None:
            # 评论我的博客
            subject = '3slab网站消息通知'
            email = self.content_object.get_email()
        else:
            # 回复评论
            subject = '3slab网站消息通知'
            email = self.reply_to.email
        if email != '':
            # text = '%s\n<a href = "%s">%s</a>'%(self.comment_text ,self.content_object.get_url(),'点击链接，查看博客')
            context = {}
            context['comment_text'] = self.comment_text
            context['url'] = self.content_object.get_url()
            text = render(None,'comment/send_email.html',context).content.decode('utf-8')
            print(text)
            send_mail = SendMail(subject,text,email)
            send_mail.start()

    def __str__(self):
        return self.comment_text
    class Meta:
        ordering = ["comment_time"]   #按照时间倒序显示

