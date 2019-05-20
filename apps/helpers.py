from functools import wraps

from django.http import HttpResponseBadRequest


def ajax_required(fun):
    """校验是否为ajax请求"""

    @wraps
    def inner(request, *args, **kwargs):
        """参考https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-editing/"""
        if not request.is_ajax():
            return HttpResponseBadRequest('不是AJAX请求!')
        return fun(request, *args, **kwargs)

    return inner


class AjaxRequired(object):
    """校验是否为ajax请求"""

    def __init__(self, fun):
        self.fun = fun

    def __call__(self, request, *args, **kwargs):
        """参考https://docs.djangoproject.com/en/2.2/topics/class-based-views/generic-editing/"""
        if not request.is_ajax():
            return HttpResponseBadRequest('不是AJAX请求!')
        return self.fun(request, *args, **kwargs)
