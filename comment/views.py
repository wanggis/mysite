from django.shortcuts import render,redirect
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse  #反向解析
from django.http import JsonResponse
from django.contrib.auth import authenticate

from .models import Comment
from.forms import CommentForm
# Create your views here.

def upload_comment(request):
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    #
    # #数据检查
    # if  not request.user.is_authenticated:
    #     return render(request, 'error.html', {'message': '用户未登录','redirect_to': referer})
    # comment_text=request.POST.get('text' ,'')
    # if comment_text =='':
    #     return render(request,'error.html',{'message':'评论不能为空哦','redirect_to': referer})
    # content_type =request.POST.get('content_type','')
    # print(content_type)
    # object_id = int(request.POST.get('object_id',''))
    # print(object_id)
    # model_class =ContentType.objects.get(model =content_type).model_class()   #得到具体的引用的模型，如获得博客模型
    # model_obj = model_class.objects.get(pk = object_id)
    #
    #
    # #检查通过，创建评论
    # comment = Comment()
    # # comment_time = models.DateTimeField(auto_now_add=True)
    # comment.user = request.user
    # comment.comment_text = comment_text
    # comment.content_object=model_obj
    # comment.save()
    #
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    # return redirect(referer)


    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST,user = request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        # comment_time = models.DateTimeField(auto_now_add=True)
        comment.user = comment_form.cleaned_data['user']
        comment.comment_text = comment_form.cleaned_data['text']
        comment.content_object=comment_form.cleaned_data['content_object']
        parent =comment_form.cleaned_data['parent']

        if  not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()


        #发送邮件通知
        comment.send_mail()

        
        data['status'] ="SUCCESS"
        data['username'] =comment.user.get_nickname_or_username()
        data['comment_time']= comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['text']= comment.comment_text
        data['content_type'] = ContentType.objects.get_for_model(comment).model
        if not parent is None:
            data['reply_to']=comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] =''
        data['pk'] =comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        #return render(request,'error.html',{'messgae':comment_form.errors,'redirect_to':referer})
        data['status'] = "ERROR"
        data['message'] = list(comment_form.errors.values())[0]
    return JsonResponse(data)



