from django.views.decorators.http import require_http_methods
from django.http.response import JsonResponse
from django.contrib.contenttypes.models import ContentType

from .models import Like
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
    try:
        content_type = ContentType.objects.get(model=content_type)
    except ContentType.DoesNotExist:
        return JsonResponse({'status': 'fail', 'msg': '点赞出错'})
    like, created = Like.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
    if created:
        is_like = True
        msg = '点赞成功'
    else:
        like.delete()
        msg = '取消点赞'
    like_num = Like.objects.filter(content_type=content_type, object_id=object_id).count()
    return JsonResponse({'is_like': is_like, 'like_num': like_num, 'status': 'success', 'msg': msg})











