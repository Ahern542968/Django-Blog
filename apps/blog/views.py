from django.shortcuts import render
from django.views.generic import View, ListView
from django.views.generic.detail import DetailView
from django.db.models import Q

from .models import Blog, BlogTag
# Create your views here.


class BlogListView(ListView):
    model = Blog
    context_object_name = 'blog_list'
    template_name = 'blog/blog-list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        tags = self.request.GET.getlist('tag')
        if not tags:
            return queryset.order_by('-date')
        sf = self.request.GET.get('sf', '-date')
        return self.get_sf_queryset(queryset, tags, sf)

    @staticmethod
    def get_sf_queryset(queryset, tags, sf):
        if sf not in ['date', '-date', 'view', '-view', 'comm', '-comm']:
            sf = '-date'
        tags_name = [tag.name for tag in BlogTag.objects.all()]
        tags = [tag for tag in tags if tag in tags_name]
        return queryset.filter(blog_tag__name__in=tags).order_by(sf)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = BlogTag.objects.all()
        context['blog_num'] = self.get_queryset().count()
        return context


class BlogDetailView(DetailView):
    model = Blog
    queryset = Blog.objects.all()
    context_object_name = 'blog'
    slug_url_kwarg = 'blog_id'
    template_name = 'blog/blog-detail.html'






