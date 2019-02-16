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
    paginate_by = 6

    def get_queryset(self):
        tags = self.request.GET.getlist('tag')
        if not tags:
            return self.model.objects.order_by('-date')
        sf = self.request.GET.get('sf', '-date')
        return self.get_sf_queryset(tags, sf)

    def get_sf_queryset(self, tags, sf):
        q = Q()
        q.connector = 'OR'
        q.children.extend(tags)
        return self.model.objects.filter(q).order_by(sf)

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






