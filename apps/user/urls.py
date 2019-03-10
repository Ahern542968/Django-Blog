from django.urls import path

from .views import UserLoginView, UserLogoutView, UserRegisterView, \
    UserResetPasswordView, SendActiveCodeView, UserActiveView, UserCenterView


urlpatterns = [
    path('center/', UserCenterView.as_view(), name='user-center'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('logout/', UserLogoutView.as_view(), name='user-logout'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('reset/', UserResetPasswordView.as_view(), name='user-reset'),
    path('active/', SendActiveCodeView.as_view(), name='blind-email'),
    path('active/<slug:code>/', UserActiveView.as_view(), name='user-active'),
]