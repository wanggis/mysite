import datetime
from django.shortcuts import render,redirect
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache   #使用单一线程
from read_statistics.utils import get_seven_days_read_data, get_today_hot_data,get_yesterday_hot_data, get_weekly_hot_blogs
from myblog.models import Blog
from django.urls import reverse  #反向解析
# def get_weekly_hot_blogs():
#     today = timezone.now().date()
#     date = today - datetime.timedelta(days=7)
#     blogs = Blog.objects.filter(read_details__date__lt=today,read_details__date__gte=date).values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')   #分组统计
#     return blogs[:5]

def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates,read_nums = get_seven_days_read_data(blog_content_type)
    #获取七天热门博客的缓存数据
    weekly_hot_data=cache.get('weekly_hot_data')
    if weekly_hot_data is None:
        weekly_hot_data = get_weekly_hot_blogs()
        cache.set('weekly_hot_data',weekly_hot_data,3600)  #1h刷新一次
    context ={}
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['weekly_hot_data'] = weekly_hot_data

    return render(request,template_name='home.html',context=context)





