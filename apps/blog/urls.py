from django.urls import path

from .views import BlogListView, BlogDetailView, SearchView
from .feeds import LastBlogFeed


urlpatterns = [
    path('feed/', LastBlogFeed(), name='feed'),
    path('', SearchView.as_view(), name='blog-search'),
    path('', BlogListView.as_view(), name='blog-list'),
    path('<slug:pk>/', BlogDetailView.as_view(), name='blog-detail'),
]
