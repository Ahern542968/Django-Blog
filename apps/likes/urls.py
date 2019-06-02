from django.urls import path

from . import views

urlpatterns = [
    path('switch_like/', views.switch_like, name='switch_like'),
]
