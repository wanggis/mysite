from django.contrib import admin
from .models import LikeRecord,LikeCount
# Register your models here.

@admin.register(LikeCount)
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('liked_num','content_object','object_id')

@admin.register(LikeRecord)
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ['id','liked_time']