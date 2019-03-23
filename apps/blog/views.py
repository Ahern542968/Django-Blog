from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.core.cache import cache

from .models import Blog, BlogTag
from comment.forms import CommentForm
from comment.models import Comment

# Create your views here.


class BlogListView(ListView):
    model = Blog
    context_object_name = 'blog_list'
    template_name = 'blog/blog-list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().filter(status=Blog.STATUS_NORMAL)
        tags = self._check_tags(self.request.GET.getlist('tag'))
        sf = self._check_sf(self.request.GET.get('sf', '-date'))
        if not tags:
            return queryset.order_by(sf)
        return queryset.filter(blog_tag__name__in=tags).order_by(sf)

    @staticmethod
    def _check_sf(sf):
        if sf not in ['date', '-date', 'views', '-views', 'comms', '-comms']:
            sf = '-date'
        return sf

    @staticmethod
    def _check_tags(tags):
        if tags:
            tags_name = [tag.name for tag in BlogTag.objects.filter(status=BlogTag.STATUS_NORMAL).only('name')]
            tags = [tag for tag in tags if tag in tags_name]
        return tags

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = BlogTag.objects.filter(status=BlogTag.STATUS_NORMAL).only('name')
        context['blog_num'] = self.model.get_blog_num()
        context['tags'] = self._check_tags(self.request.GET.getlist('tag'))
        context['sf'] = self._check_sf(self.request.GET.get('sf', ''))
        return context


class BlogDetailView(DetailView):
    model = Blog
    queryset = Blog.objects.filter(status=Blog.STATUS_NORMAL)
    context_object_name = 'blog'
    slug_url_kwarg = 'blog_id'
    template_name = 'blog/blog-detail.html'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        self.handle_views()
        return response

    def handle_views(self):
        increase_views = False
        uid = self.request.uid
        views_key = 'views:%s:%s' % (uid, self.request.path)
        if not cache.get(views_key):
            increase_views = True
            cache.set(views_key, 1, 60*60*24)
        if increase_views:
            self.object.add_views()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['prev_blog'] = self.queryset.filter(id__lt=self.object.id).order_by('-id').first()
        context['next_blog'] = self.queryset.filter(id__gt=self.object.id).order_by('id').first()
        context['comments'] = self.object.comment_set.\
            filter(status=Comment.STATUS_NORMAL, r_comment=None).order_by('-date')
        context['form'] = CommentForm(initial={'blog': self.object, 'p_comment_id': 0})
        return context


# 原来使用django继承实现, 已改用django-haystack，先注释
# class SearchView(BlogListView):
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context.update({
#             'search': self.request.GET.get('search')
#         })
#         return context
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         search = self.request.GET.get('search', '')
#         if search:
#             queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
#         return queryset
