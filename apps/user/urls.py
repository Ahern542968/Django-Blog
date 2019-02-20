from django.urls import path
from django.contrib.auth import views as auth_views

from .views import UserLoginView


urlpatterns = [
    path('login/', UserLoginView.as_view(), name='login'),
]