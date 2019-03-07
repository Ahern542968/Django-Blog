from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class BlogAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget(), label='正文', required=True)
