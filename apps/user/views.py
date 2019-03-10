from datetime import datetime

from django.conf.global_settings import LOGIN_REDIRECT_URL
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetConfirmView
from django.views.generic.edit import FormView
from django.urls import resolve, reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login

from .forms import UserLoginForm, UserRegisterForm, UserResetPasswordForm
from .models import UserActiveCode
from utils.send_mail import send_html_email, generate_active_code
# Create your views here.

User = get_user_model()


class UserLoginView(LoginView):
    template_name = 'user/user-login.html'
    authentication_form = UserLoginForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().get(request, *args, **kwargs)


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'user/user-register.html'
    success_url = reverse_lazy('blog:blog-list')

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class SendActiveCodeView(TemplateView):
    template_name = 'user/user-template.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if not user.is_authenticated or user.is_active:
            return HttpResponseRedirect(resolve(LOGIN_REDIRECT_URL))
        if UserActiveCode.objects.filter(email=user.email).exists():
            if (datetime.now() - UserActiveCode.objects.filter(email=user.email)
                    .order_by('-date').first().date).seconds <= 180:
                context['title'] = 'The mail is sent too frequently. If you have not received the email, please ' \
                                   'contact the blogger within 5 minutes.'
                return context
        code = generate_active_code()
        subject = u"[Ahern's Blog]Account Active"
        html_content = u'<p>Please open this link to active your account：</p>' \
                       u'<a href="#">http://127.0.0.1:8000/user/active/{code}</a>.'.format(code=code)
        email = user.email
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
        code = self.kwargs.get('code', '')
        if not code:
            context['title'] = 'Your account activation link has expired.'
            return context
        active_codes = UserActiveCode.objects.filter(code=code, send_for=UserActiveCode.FOR_BLIND_EMAIL)
        if active_codes.exists():
            for active_code in active_codes:
                email = active_code.email
                user = User.objects.get(email=email)
                user.is_active = True
                user.save()
                active_code.delete()
                context['title'] = 'Your account has been activated successfully.'
        else:
            context['title'] = 'Your account activation link has expired.'
        return context


class UserResetPasswordView(PasswordResetConfirmView):
    form_class = UserResetPasswordForm
    template_name = 'user/user-reset.html'
    success_url = reverse_lazy('blog:blog-list')


class UserLogoutView(LogoutView):
    next_page = 'user:user-login'


class UserCenterView(LoginRequiredMixin, TemplateView):
    template_name = 'user/user-center.html'

