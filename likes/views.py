from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.http import JsonResponse
from django.db.models import ObjectDoesNotExist
from .models import LikeCount,LikeRecord

# Create your views here.

def SuccessResponse(liked_num):
    data={}
    data['status'] = 'SUCCESS'
    data['liked_num'] = str(liked_num)
    return JsonResponse(data)

def ErrorResponse(code, message):
    data={}
    data['code'] = code
    data['status'] = 'ERROR'
    data['message'] = message
    return JsonResponse(data)

def like_change(request):

    #获取数据
    user = request.user
    if not user.is_authenticated:
        return ErrorResponse(400,'你还没有登录')
    content_type = request.GET.get('content_type')
    object_id = int(request.GET.get('object_id'))

    try:
        content_type = ContentType.objects.get(model = content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return ErrorResponse(401,"对象不存在")

    #处理数据
    if request.GET.get('is_like') =='true':
        #要点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type,object_id=object_id,user=user)
        if created:
            #未点赞过，进行点赞
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.liked_num +=1
            like_count.save()
            return SuccessResponse(like_count.liked_num)
        else:
            #已经点赞，不能重复点赞
            return ErrorResponse(402,'重复点赞')
    else:
        #要取消点赞
        if LikeRecord.objects.filter(content_type = content_type,object_id = object_id,user =user).exists():
            #有点赞果，取消点赞
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            #点赞总数减一
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type,object_id = object_id)
            if not created:
                like_count.liked_num-=1
                like_count.save()
                return SuccessResponse(like_count.liked_num)
            else:
                return ErrorResponse(402, '数据错误')

        else:
            #没有点赞过，不能取消
            return ErrorResponse(403, '你未曾点赞')




