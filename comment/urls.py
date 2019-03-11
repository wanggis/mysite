from django.conf.urls import url
from django.urls import path
from . import views


app_name = 'comment'
urlpatterns = [
    url(r'^upload_comment/$', views.upload_comment, name='upload_comment'),

]