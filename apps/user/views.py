from datetime import datetime

from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView
from django.urls import resolve
from django.http import HttpResponseRedirect

from DjangoBlog.settings import LOGIN_REDIRECT_URL
from .forms import UserLoginForm, UserRegisterForm
from .models import UserActiveCode
from utils.send_mail import send_html_email, generate_active_code
# Create your views here.

User = get_user_model()


class UserLoginView(LoginView):
    template_name = 'user/user-login.html'
    authentication_form = UserLoginForm


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'user/user-register.html'
    success_url = 'blog:blog-detail'


class SendActiveCodeView(TemplateView):
    template_name = 'user/user-template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_authenticated or user.is_active:
            return HttpResponseRedirect(resolve(LOGIN_REDIRECT_URL))
        if (datetime.now() - UserActiveCode.objects.get(user.email).date).minutes() <= 5:
            context['title'] = 'The mail is sent too frequently. If you have not received the email, please contact ' \
                               'the blogger within 5 minutes.'
        else:
            code = generate_active_code()
            subject = u"[Ahern's Blog]Account Active"
            html_content = u'<p>Please open this link to active your account：</p>' \
                           u'<a href="#">http://127.0.0.1:8000/user/active/{code}</a>.'.format(code=code)
            email = [user.email]
            send_html_email(subject, html_content, email)

            user_active_code = UserActiveCode()
            user_active_code.code = code
            user_active_code.email = email
            user_active_code.send_for = UserActiveCode.FOR_BLIND_EMAIL
            user_active_code.save()
            context['title'] = 'The mail has been sent, please check it.'
        return context


class UserActiveView(TemplateView):
    template_name = 'user/user-template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        code = self.request.code
        active_codes = UserActiveCode.objects.filter(code=code, send_for=UserActiveCode.FOR_BLIND_EMAIL)
        if active_codes.exists():
            for active_code in active_codes:
                email = active_code.email
                user = User.objects.get(email=email)
                user.is_active = True
                active_code.delete()
                context['title'] = 'Your account has been activated successfully.'
        else:
            context['title'] = 'Your account activation link has expired.'
        return context
