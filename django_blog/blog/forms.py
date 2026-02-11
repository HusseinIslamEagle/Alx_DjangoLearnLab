from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """
    ModelForm for creating and updating posts.
    """

    class Meta:
        model = Post
        fields = ['title', 'content']
