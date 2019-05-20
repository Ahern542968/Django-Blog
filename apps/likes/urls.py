from django.urls import path

from . import views

urlpatterns = [
    path('change_like/', views.change_like, name='change_like'),
]
