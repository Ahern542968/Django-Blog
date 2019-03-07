from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.feedgenerator import Rss201rev2Feed
from .models import Blog


class LastBlogFeed(Feed):
    title = 'Blog System'
    feed_type = Rss201rev2Feed
    link = '/feed/'
    description = "It's is a blog system power by django"

    def items(self):
        return Blog.objects.filter(status=Blog.STATUS_NORMAL).order_by('-date')[:10].only('title', 'date')

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return reverse('blog:blog-detail', args=[item.pk])
