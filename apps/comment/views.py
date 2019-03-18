from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .forms import CommentForm
from .models import Comment

# Create your views here.


@method_decorator(require_POST, name='dispatch')
class CommentView(CreateView):
    model = Comment
    form_class = CommentForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        p_comment_id = self.request.POST.get('p_comment_id')
        if p_comment_id == '0':
            self.object.p_comment = None
            self.object.r_comment = None
            self.object.r_user = None
        else:
            p_comment = Comment.objects.get(id=p_comment_id)
            self.object.p_comment = p_comment
            self.object.r_user = p_comment.c_user
            if p_comment.r_comment:
                self.object.r_comment = p_comment.r_comment
            else:
                self.object.r_comment = p_comment
        self.object.c_user = self.request.user
        self.object.blog.add_comms()
        self.object.save()

        if self.object.r_comment:
            root_id = self.object.r_comment.id
            r_user = self.object.r_user.get_name
        else:
            root_id = self.object.id
            r_user = ''

        data = {
            'status': 'success',
            'msg': 'Comment successful',
            'c_user': self.object.c_user.get_name,
            'date': self.object.date.strftime('%Y-%m-%d %H:%M'),
            'content': self.object.content,
            'id': self.object.id,
            'root_id': root_id,
            'r_user': r_user,
        }
        return JsonResponse(data)

    def form_invalid(self, form):
        data = {
            'status': 'error',
            'msg': list(form.errors.values())[0][0],
        }
        return JsonResponse(data)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'user': self.request.user,
        })
        return kwargs


class LatestCommentViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'latest_comments': Comment.objects.filter(status=Comment.STATUS_NORMAL).order_by('-date')[:5]
        })
        return context
