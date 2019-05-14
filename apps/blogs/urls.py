from django.urls import path

from .views import BlogListView, BlogDetailView

urlpatterns = [
    path('', BlogListView.as_view(), name='list'),
    path('<str:slug>/', BlogDetailView.as_view(), name='detail'),
]
