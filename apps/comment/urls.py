from django.urls import path

from .views import CommentView


urlpatterns = [
    path('create_comment', CommentView.as_view(), name='create-comment'),
]
