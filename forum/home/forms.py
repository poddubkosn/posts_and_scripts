from django import forms
from .models import Comment, Post
from ckeditor.widgets import CKEditorWidget 


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'group', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
