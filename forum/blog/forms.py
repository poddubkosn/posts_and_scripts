from django import forms
from .models import MyScripts, Comment


class MyscriptsForm(forms.ModelForm):
    class Meta:
        model = MyScripts
        fields = ('title', 'text', 'image')


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )

