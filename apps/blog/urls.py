from django.urls import path

from blog.views import BlogListView, BlogDetailView


urlpatterns = [
    path('', BlogListView.as_view(), name='blog-list'),
    path('<slug:pk>/', BlogDetailView.as_view(), name='blog-detail'),
]
