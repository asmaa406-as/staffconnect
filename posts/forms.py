from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    """Used by both CreateView and UpdateView. Slug is auto-generated."""

    class Meta:
        model = Post
        fields = ['title', 'body']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Announcement title'}),
            'body': forms.Textarea(attrs={'rows': 8, 'placeholder': 'Write your announcement...'}),
        }
