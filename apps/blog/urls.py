from django.urls import path, include

from blog.views import HomeView, BlogListView


urlpatterns = [
    # path('blog/', HomeView.as_view(), name='blog_list'),
    path('list/', BlogListView.as_view(), name='blog_list'),
]
