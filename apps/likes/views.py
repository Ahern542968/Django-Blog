from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

from .models import Like
from helpers import AjaxRequired
# Create your views here.


@AjaxRequired
@login_required
@require_http_methods(['POST'])
def switch_like(request):
    """先是否post方法"""
    user = request.user
    content_type = request.POST.get('object_type')
    object_id = request.POST.get('object_id')
    is_like = False
    content_type = get_object_or_404(ContentType, model=content_type)
    like, created = Like.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
    if created:
        is_like = True
        msg = '点赞成功'
    else:
        like.delete()
        msg = '取消点赞'
    like_num = Like.objects.get_like_num(content_type=content_type, object_id=object_id)
    return JsonResponse({'is_like': is_like, 'like_num': like_num, 'msg': msg})
