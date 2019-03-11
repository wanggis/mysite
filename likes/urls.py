from django.conf.urls import url
from django.urls import path
from . import views

app_name = 'likes'

urlpatterns = [
    url(r'^like_change', views.like_change, name='like_change'),
]