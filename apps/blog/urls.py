from django.urls import path, include

from blog.views import HomeView


urlpatterns = [
    path('list/', HomeView.as_view(), name='blog_list'),
]
