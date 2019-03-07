from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Blog


class BlogSitemap(Sitemap):
    changefreq = 'always'
    priority = 1.0
    protocol = 'https'

    def items(self):
        return Blog.objects.filter(status=Blog.STATUS_NORMAL).only('title', 'date', 'id')

    def lastmod(self, obj):
        return obj.date

    def location(self, obj):
        return reverse('blog:blog-detail', args=[obj.pk])
