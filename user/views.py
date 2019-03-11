import datetime
import time
import string
import random
from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache   #使用单一线程
from django.contrib import auth
from django.contrib.auth import authenticate,login  #登录和身份验证
from django.urls import reverse  #反向解析
from .forms import LoginForm,RegForm,ChangeNicknameForm,BindEmailForm,ChangePasswordFrom,ForgotPasswordForm
from django.contrib.auth.models import User
from django.http import JsonResponse
from .models import Profile
from django.core.mail import send_mail



def login_user(request):
    # username = request.POST.get('username','')
    # password = request.POST.get('password', '')
    # user = authenticate(request,username = username, password =password)  #验证登录用户是否进行过注册
    # referer = request.META.get('HTTP_REFERER',reverse('home'))  #用来获取你是从哪个页面传数据过来的，如果得到，就返回这个页面；如果得不到，则反向解析，默认为首页，，得到链接'/'
    # print(referer)
    # if user is not None:
    #     login(request,user)
    #     #Redirect to a success page  重定向到一个登录成功的界面
    #     return redirect(referer)
    #
    # else:
    #     return render(request,'error.html',{'message':'用户名或密码不正确，无法登录哦'})

    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():  # 验证提交的数据是否为空
            # #如果返回true，则说明数据不为空
            # username = login_form.cleaned_data['username']
            # password = login_form.cleaned_data['password']
            # user = authenticate(request, username=username, password=password)  # 验证登录用户是否进行过注册
            # if user is not None:
            user = login_form.cleaned_data['user']
            # 如果该用户已经注册过（即存在）
            login(request, user)  # 登录用户
            # Redirect to a success page  重定向到一个登录成功的界面
            return redirect(request.GET.get('from', reverse('home')))  # 获取之前跳转的路径
        # else:
        #     login_form.add_error(None,'用户名或者密码不正确')   #收集错误信息
        #     context = {}
        #     context['login_form'] = login_form
        #     return render(request, 'login.html', context)
    else:
        login_form = LoginForm()
    context = {}
    context['login_form'] = login_form
    return render(request, 'user/login.html', context)


def login_for_modal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():  # 验证提交的数据是否为空
        user = login_form.cleaned_data['user']
        login(request, user)  # 登录用户
        data['status'] = "SUCCESS"
    else:
        data['status'] = "ERROR"
    print(data)
    return JsonResponse(data)


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def register_user(request):
    if request.method == 'POST':
        reg_form = RegForm(request.POST,request = request)
        if reg_form.is_valid():  # 验证提交的数据是否为空
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            #清楚session
            del request.session['register_code']
            # 登录用户
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(request.GET.get('from', reverse('home')))

    else:
        reg_form = RegForm()
    context = {}
    context['reg_form'] = reg_form
    return render(request, 'user/register.html', context)


def user_info(request):
    context = {}
    return render(request, 'user/user_info.html', context)


def change_nickname(request):
    return_to = request.GET.get('from', reverse('home'))
    if request.method=="POST":
       form  = ChangeNicknameForm(request.POST,user=request.user)
       if form.is_valid():
           nickname_new = form.cleaned_data['nickname_new']
           profile,created = Profile.objects.get_or_create(user = request.user)
           profile.nick_name = nickname_new
           profile.save()
           return redirect(return_to)
    else:
        form =ChangeNicknameForm()

    context ={}
    context['page_title'] ="修改昵称"
    context['form_title'] = "修改昵称"
    context['submit_text'] ="修改"
    context['form'] = form
    context['return_back_url'] =return_to
    return render(request,'form.html',context)

def bind_email(request):
    return_to = request.GET.get('from', reverse('home'))  #重定向
    if request.method == "POST":
        form = BindEmailForm(request.POST, request=request)
        if form.is_valid():
            email = form.cleaned_data['email']
            request.user.email = email
            request.user.save()
            # 清除session
            del request.session['bind_email_code']
            return redirect(return_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = "绑定邮箱"
    context['form_title'] = "绑定邮箱"
    context['submit_text'] = "绑定"
    context['form'] = form
    context['return_back_url'] = return_to
    return render(request, 'user/bind_email.html', context)


def send_verification_code(request):
    email = request.GET.get('email','')
    print(email)
    send_for = request.GET.get('send_for','')
    data={}

    if email !="":
        #生成验证码
        code = ''.join(random.sample(string.ascii_letters+string.digits,4))
        request.session['bind_email_code'] = code
        now = int(time.time())
        send_code_time = request.session.get('send_code_time', 0)
        if now - send_code_time < 60:
            data['status'] = 'ERROR'
        else:
            request.session[send_for] = code
            request.session['send_code_time'] = now
        #发送邮件
            send_mail(
                # 'Subject here',
                # 'Here is the message.',
                # 'from@example.com',
                # ['to@example.com'],
                # fail_silently=False,
                '绑定邮箱',
                '验证码: %s' % code,
                '3463854346@qq.com',
                [email],
                fail_silently=False,
            )
            data['status']="SUCCESS"
    else:
        data["status"]="ERROR"
    return JsonResponse(data)



def change_password(request):
    return_to = reverse('home')
    if request.method == "POST":
        form = ChangePasswordFrom(request.POST, user=request.user)
        if form.is_valid():
            user = request.user
            old_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            user.set_password(new_password)
            user.save()
            auth.logout(request)
            return redirect(reverse('home'))
    else:
        form = ChangePasswordFrom()

    context = {}
    context['page_title'] = "修改密码"
    context['form_title'] = "修改密码"
    context['submit_text'] = "修改"
    context['form'] = form
    context['return_back_url'] = return_to
    return render(request, 'form.html', context)

def forgot_password(request):
    return_to =  reverse('home')  # 重定向
    if request.method == "POST":
        form = ForgotPasswordForm(request.POST, request=request)
        if form.is_valid():
            email  = form.cleaned_data['email']
            new_password = form.cleaned_data['new_password']
            user = User.objects.get(email = email)
            user.set_password(new_password)
            user.save()
            # 清除session
            del request.session['forgot_password_code']
            return redirect(return_to)
    else:
        form = BindEmailForm()

    context = {}
    context['page_title'] = "重置密码"
    context['form_title'] = "重置密码"
    context['submit_text'] = "重置"
    context['form'] = form
    context['return_back_url'] = return_to
    return render(request, 'user/forgot_password.html', context)
