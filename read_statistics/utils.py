import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum
from .models import ReadNum,ReadDetail
from myblog.models import Blog


#提取公共部分，简化代码

def read_statistics_once_read(request,obj):
    ct = ContentType.objects.get_for_model(obj)
    key = '%s_%s_read' %(ct.model,obj.pk)
    # 如果无法获得cookie的键值，则加一
    if not  request.COOKIES.get(key):
       
        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     #存在记录
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # else:
        #     # 不存在对应的记录,进行实例化
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)
        #总阅读数加一
        #函数：get_or_create，存在就get，不存在就create
        readnum,created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        #阅读量计数加一
        readnum.read_num +=1
        readnum.save()

        #统计当天的某一个博客的阅读数量
        date = timezone.now().date()
        # if ReadDetail.objects.filter(content_type=ct,object_id=obj.pk,date=date).count():
        #     readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date).count()
        # else:
        #     readDetail =  ReadDetail()
        readDetail, created=ReadDetail.objects.get_or_create(content_type=ct, object_id=obj.pk, date=date)
        readDetail.read_num += 1
        readDetail.save()
    return key

#七天，每一天的阅读量的汇总
def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    dates =[]
    read_nums =[]
    for i in range(7,0,-1):
        date = today - datetime.timedelta(days=i)
        dates.append(date.strftime('%y/%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type,date=date)
        result = read_details.aggregate(read_num_sum =Sum('read_num'))  #聚合函数
        read_nums.append(result['read_num_sum'] or 0)  #会做一个判断，如果是None，则为false，用0代替
        
    return dates,read_nums



def get_today_hot_data(content_type):
    today = timezone.now().date()
    blogs = Blog.objects.filter(read_details__date=today).values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')  # 分组统计
    return blogs[:5]

def get_yesterday_hot_data(content_type):
    yesterday = timezone.now().date()- datetime.timedelta(days=1)
    # read_details = ReadDetail.objects.filter(content_type=content_type,date=yesterday).order_by('-read_num') #倒序排序，由大到小
    # return read_details[:5]
    blogs = Blog.objects.filter(read_details__date=yesterday).values('id', 'title').annotate(
        read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')  # 分组统计
    return blogs[:5]
#
# def get_week_hot_data(content_type):
#     today = timezone.now().date()
#     date = today - datetime.timedelta(days=7)
#     read_details = ReadDetail.objects.filter(content_type=content_type, date__lt=today,date__gte=date).values('content_type','object_id').annotate(read_sum_num=Sum('read_num')).order_by('-read_sum_num')  # 倒序排序，由大到小
#     return read_details[:5]

#七天内，每一篇博客的阅读量汇总
def get_weekly_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today,read_details__date__gte=date).values('id', 'title').annotate(read_num_sum=Sum('read_details__read_num')).order_by('-read_num_sum')   #分组统计
    return blogs[:5]


