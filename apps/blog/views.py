from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from django.core.cache import cache

from .models import Blog, BlogTag
from comment.forms import CommentForm
from comment.views import LatestCommentViewMixin
# Create your views here.


class RecommendViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'recommends': Blog.get_topped_blogs()
        })
        return context


class LatestBlogViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'latest_blogs': Blog.get_latest_blogs()
        })
        return context


class RightPartViewMixin(RecommendViewMixin, LatestBlogViewMixin):
    pass


class BlogListView(RightPartViewMixin, LatestCommentViewMixin, ListView):
    model = Blog
    context_object_name = 'blog_list'
    template_name = 'blog/blog-list.html'
    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset().filter(status=Blog.STATUS_NORMAL)
        tags = self.request.GET.getlist('tag')
        if not tags:
            return queryset.order_by('-date')
        sf = self.request.GET.get('sf', '-date')
        return self._get_sf_queryset(queryset, tags, sf)

    @staticmethod
    def _get_sf_queryset(queryset, tags, sf):
        if sf not in ['date', '-date', 'views', '-views', 'comms', '-comms']:
            sf = '-date'
        tags_name = [tag.name for tag in BlogTag.objects.filter(status=BlogTag.STATUS_NORMAL).only('name')]
        tags = [tag for tag in tags if tag in tags_name]
        return queryset.filter(blog_tag__name__in=tags).order_by(sf)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = BlogTag.objects.filter(status=BlogTag.STATUS_NORMAL).only('name')
        context['blog_num'] = self.get_queryset().count()
        context['tags'] = self.request.GET.getlist('tag')
        return context


class BlogDetailView(RecommendViewMixin, LatestBlogViewMixin, LatestCommentViewMixin, DetailView):
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
        context['comments'] = self.object.comment_set.all()
        context['form'] = CommentForm(initial={'blog': self.object})
        return context


class SearchView(BlogListView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'search': self.request.GET.get('search')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search', '')
        if search:
            queryset = queryset.filter(Q(title__icontains=search) | Q(content__icontains=search))
        return queryset
