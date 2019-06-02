from django.views.decorators.http import require_http_methods
from django.http.response import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from .models import Like
from notifications.views import notification_handler
# Create your views here.


@require_http_methods(['POST'])
def change_like(request):
    """先是否post方法"""
    user = request.user
    if not user.is_authenticated:
        return JsonResponse({'status': 'fail', 'msg': '用户未登录'})
    content_type = request.POST.get('object_type')
    object_id = request.POST.get('object_id')
    is_like = False
    content_type = get_object_or_404(ContentType, model=content_type)
    like, created = Like.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
    if created:
        is_like = True
        msg = '点赞成功'
        recipient = like.like_object.author.author if hasattr(like.like_object, 'author') else like.like_object.user
        notification_handler(user, recipient.username, 'L', like.like_object, id_value=object_id, key='social_update')
    else:
        like.delete()
        msg = '取消点赞'
    like_num = Like.objects.count_like(content_type=content_type, object_id=object_id)
    return JsonResponse({'is_like': is_like, 'like_num': like_num, 'status': 'success', 'msg': msg})











