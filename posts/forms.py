from django import forms
from .models import Post, Comment
from groups.models import Group
from flask import request
class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Post
        fields = ('content', 'group', 'image')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', 
                            widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))
    class Meta:
        model = Comment
        fields = ('body',)