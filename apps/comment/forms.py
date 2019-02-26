from django.forms import ModelForm, widgets

from .models import Comment


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['blog', 'content']

