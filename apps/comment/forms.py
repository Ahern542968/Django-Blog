from django.forms import ModelForm, widgets

from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['blog', 'content']
        widgets = {
            'blog': widgets.HiddenInput,
            'parent_com': widgets.HiddenInput,
            'content': widgets.Textarea(attrs={
                'id': 'comment-content',
                'placeholder': '想对作者说点什么',
                'class': 'comment-content'
            })
        }
