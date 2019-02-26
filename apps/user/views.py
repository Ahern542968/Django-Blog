from django.contrib.auth.views import LoginView
from django.views.generic.edit import FormView

from .forms import UserLoginForm, UserRegisterForm
# Create your views here.


class UserLoginView(LoginView):
    template_name = 'user/user-login.html'
    authentication_form = UserLoginForm


class UserRegisterView(FormView):
    form_class = UserRegisterForm
    template_name = 'user/user-register.html'
    success_url = 'blog:blog-detail'















