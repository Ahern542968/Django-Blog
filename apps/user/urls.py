from django.urls import path

from .views import UserLoginView, UserRegisterView, SendActiveCodeView, UserActiveView


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('active/', SendActiveCodeView.as_view(), name='blind-email'),
    path('active/<slug:code>/', UserActiveView.as_view(), name='user-active'),
]