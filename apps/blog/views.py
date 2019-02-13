from django.shortcuts import render
from django.views.generic import View, ListView
from django.db.models import Count

from .models import Blog, BlogTag
# Create your views here.


class HomeView(View):
    def get(self, request):
        return render(request, 'blog/blog_list.html', {})


class BlogListView(ListView):
    model = Blog
    queryset = Blog.objects.order_by('-created_date')
    context_object_name = 'blog_list'
    template_name = 'blog/blog_list.html'
    paginate_by = 1

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = BlogTag.objects.all()
        return context

