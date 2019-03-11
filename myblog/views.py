from django.shortcuts import render,get_object_or_404
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from datetime import datetime
from read_statistics.utils import read_statistics_once_read
from .models import Blog,BlogType
from comment.models import Comment
from comment.forms import CommentForm
from user.forms import LoginForm
# Create your views here.



#一个公共函数，提取出每一个视图函数的公共部分
def get_blog_lists_common_data(blogs_all_list,request):
    paginator = Paginator(blogs_all_list, settings.BLOGS_NUM_OF_EACH_PAGE)  # 实例化分页器，每十页进行分页
    page_num = request.GET.get('page', 1)  # 获取url页码参数，在python中，get请求得到是一个请求参数的字典，访问其中的'page'属性，如果没有给定值，就默认page属性的值为1
    page_of_blogs = paginator.get_page(page_num)  # 该函数会对参数类型进行判断和转换，一旦出错，会自动默认为1
    current_page_num = page_of_blogs.number  # 获取当前页码
    # 获取当前页码的前后两页的页码范围
    page_range = list(range(max(current_page_num - 2, 1), current_page_num)) + list(
        range(current_page_num, min(current_page_num + 2, paginator.num_pages) + 1))

    # 加上省略页码标记
    if page_range[0] - 1 >= 2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')

    # 加上首页和尾页
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    #获取博客分类的对应博客数量


    # blog_types = BlogType.objects.all()
    # blog_type_list=[]
    # for blog_type in blog_types:
    #     blog_type.blog_count=Blog.objects.filter(blog_type=blog_type).count()   #利用python语言规则：实例化对象，增加一个count数量属性
    #     blog_type_list.append(blog_type)

    #获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict ={}
    for blog_date in blog_dates:
        blog_date_count = Blog.objects.filter(created_time__year = blog_date.year,
                            created_time__month = blog_date.month).count()
        blog_dates_dict[blog_date]=blog_date_count


    context = {}
    # context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types'] =  BlogType.objects.annotate(blog_count = Count('blog_blog'))  #解析出来的是一条SQL语句，只有在用的时候，才会执行SQL语句，将数据放入内存,会减轻服务器的压力
    context['page_range'] = page_range
    context['blog_dates'] = blog_dates_dict  #
    return context

def blog_list(request):
    blogs_all_list= Blog.objects.all()

    context = get_blog_lists_common_data(blogs_all_list,request)
    # 用于计算一共有几篇博客context['blogs_count'] =Blog.objects.all().count()
    return render(request, template_name='myblog/blog_list.html', context=context)

def blog_detail(request,blog_pk):
    context = {}
    blog= Blog.objects.get(pk=blog_pk)
    #计算统计博客的阅读数量
    read_cookie_key = read_statistics_once_read(request,blog)
    
    #获取这篇博客的相关评论
    blog_content_type = ContentType.objects.get_for_model(blog)  #获得评论对象的模型
    # comments = Comment.objects.filter(content_type = blog_content_type,object_id = blog.pk,parent=None)
    

    #假设这一篇博客是1/26
    context['previous_blog']  = Blog.objects.filter(created_time__gt=blog.created_time).last()  #获得紧挨着的上一篇博客1/27
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 获得紧挨着的下一篇博客1/25
    context['blog']=blog
    # context['login_form'] = LoginForm()
    # context['comments'] = comments.order_by('-comment_time')
    # context['comment_count'] = Comment.objects.filter(content_type = blog_content_type,object_id = blog.pk).count()
    # context['comment_form']=CommentForm(initial={'content_type': blog_content_type.model,'object_id':blog_pk,'reply_comment_id':0})   #显示评论的表单
    response=render(request, template_name='myblog/blog_detail.html', context=context)   #响应,会自动包含用户信息，详细见settings---Templates
    response.set_cookie( read_cookie_key, 'true')  #阅读cookie的标记，默认是在退出浏览器之前，维持一次通话
    return response


def blogs_with_type(request,blog_type_pk):
    context = {}
    blog_type= get_object_or_404(BlogType,pk=blog_type_pk)  #主键等于参数传进来的值
    blogs_type_list =Blog.objects.filter(blog_type=blog_type)  #进行筛选
    context = get_blog_lists_common_data(blogs_type_list,request)
    context['blog_type'] = blog_type
    return render(request,template_name='myblog/blogs_with_type.html',context=context)

def blogs_with_date(request,year,month):
    context = {}
    # blog_type = get_object_or_404(BlogType, pk=blog_type_pk)  # 主键等于参数传进来的值
    blogs_date_list = Blog.objects.filter(created_time__year=year,created_time__month=month)  # 进行筛选

    context=get_blog_lists_common_data(blogs_date_list,request)
    context['blogs_with_date'] = '%s年%s月' %(year,month)
    return render(request,template_name='myblog/blogs_with_date.html', context=context)