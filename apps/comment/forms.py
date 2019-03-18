from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    p_comment_id = forms.IntegerField(widget=forms.HiddenInput, required=False)

    class Meta:
        model = Comment
        fields = ['content', 'blog', 'p_comment_id']
        widgets = {
            'blog': forms.HiddenInput(),
            'content': forms.Textarea(
                attrs={'class': 'comment-content', 'placeholder': 'What do you want to say to the author'},
            ),
        }

    def __init__(self, *args, **kwargs):
        if 'user' in kwargs:
            self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)

    def clean_p_comment_id(self):
        p_comment_id = self.cleaned_data['p_comment_id']
        if (p_comment_id != 0) and (not Comment.objects.filter(id=p_comment_id).exists()):
            raise forms.ValidationError('Comment object does not exist')
        return self.cleaned_data

    def clean(self):
        if not self.user.is_authenticated:
            raise forms.ValidationError('Please log in first')
        if not self.user.is_active:
            raise forms.ValidationError('Please activate the user first')
        return self.cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=False)
        if commit:
            instance.save()
        return instance
