from django.contrib import admin
from .models import BlogType,Blog#,ReadNum
# Register your models here.

@admin.register(BlogType)
class BlogtypeAdmin(admin.ModelAdmin):
    list_display = ('id','type_name')

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id','title','blog_type','get_read_num','author','created_time','last_update_time')
    search_fields = ['title']
