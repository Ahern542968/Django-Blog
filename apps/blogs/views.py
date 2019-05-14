from django.views.generic import ListView, DetailView

from .models import Blog, Tag
# Create your views here.


class TagCloudMixin:
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'tags_cloud': Blog.objects.get_tags_cloud(),
            'blog_publish_counted': Blog.objects.get_publish().count()
        })
        return context


class BlogListView(TagCloudMixin, ListView):
    """已发布的文章列表"""
    model = Blog
    paginate_by = 5
    context_object_name = 'blogs'
    template_name = 'blogs/blogs_list.html'
    tag = None

    def get_queryset(self):
        return Blog.objects.get_publish(tag=self.tag) if self.get_tag() else Blog.objects.get_publish()

    def get_tag(self):
        self.tag = self.request.GET.dict().get('tag')
        return self.tag if self.tag in Tag.objects.names() else None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['tag'] = self.tag
        return context


class BlogDetailView(TagCloudMixin, DetailView):
    model = Blog
    context_object_name = 'blog'
    template_name = 'blogs/blogs_detail.html'


