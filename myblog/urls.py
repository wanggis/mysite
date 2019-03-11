from django.conf.urls import url
from django.urls import path
from . import views


app_name = 'myblog'
urlpatterns = [
    url(r'^$', views.blog_list, name='blog_list'),
    url(r'^(?P<blog_pk>[0-9]+)/$', views.blog_detail, name='blog_detail'),
    url(r'^type/(?P<blog_type_pk>[0-9]+)/$', views.blogs_with_type, name='blogs_with_type'),
    url(r'^date/(?P<year>[0-9]+)/(?P<month>[0-9]+)',views.blogs_with_date, name ='blogs_with_date')

]
#将根urlconf指向polls.urls模块
#该url函数传递了四个参数，两个必须：route 和view ，以及两个可选kwargs和name
    #route参数：使用正则表达式进行捕获和匹配
        # 术语 “regex” 是正则表达式 “regular expression” 的缩写，是匹配字符串的一段语法，像这里例子的是 url 匹配模式。Django 从列表的第一个正则表达式开始，按顺序匹配请求的 URL，直到找到与之匹配的。
        # 注意，这些正则表达式不会去匹配 GET 和 POST 请求的参数值，或者域名。
        # 比如 https://www.example.com/myapp/ 这个请求，URLconf 会找 myapp/；https://www.example.com/myapp/?page=3 这个请求，URLconf 同样只会找 mysqpp/。
        #这些正则表达式在 URLconf 模块加载后的第一时间就被编译了
    #view参数
        # 当Django发现一个正则表达式匹配时，Django就会调用指定的视图函数，
        # HttpRequest对象作为第一个参数，正则表达式捕获的值作为其他参数。如果正则使用简单捕获，值会作为位置参数传递；
        # 如果使用命名捕获，值会作为关键字传递。我们稍后会给出一个例子。
    # name参数
        #命名你的URL可以让你在Django的别处明白引用的是什么，特别是在模版里。
        #这个强大的特性允许你在项目里对一个文件操作就能对URL模式做全局改变。