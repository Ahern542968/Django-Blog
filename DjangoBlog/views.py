from DjangoBlog.settings import LOGIN_REDIRECT_URL
from django.views.generic.base import View
from django.shortcuts import redirect, reverse


class IndexView(View):
    def get(self, request):
        return redirect(reverse(LOGIN_REDIRECT_URL))
