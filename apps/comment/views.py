from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST

from .forms import CommentForm
from .models import Comment

# Create your views here.


@method_decorator(require_POST, name='dispatch')
class CommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/blog-detail.html'
    login_url = 'user:login'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:blog-detail', args=[str(self.object.blog.id)])
