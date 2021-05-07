from django import forms
from .models import Post, Comment,BadWord
from django.core.exceptions import ValidationError
class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
    class Meta:
        model = Post
        fields = ('content', 'group', 'image')
        
    def clean_content(self):
        content = self.cleaned_data.get('content')
        bad_words = BadWord.objects.all()
        results = list(map(lambda x: x.word, bad_words))
        content_list = content.split()
        bad_words_list = []
        for word in results:
            if word in content_list:
                bad_words_list.append(word)
        bad_words_string = ', '.join(bad_words_list)
        print("bad_words_list = ",bad_words_list)
        print("bad_words_string = ",bad_words_string)
        if len(bad_words_list) > 0:
            raise ValidationError("The content of a post contain bad words " + bad_words_string)
        return content

class CommentModelForm(forms.ModelForm):
    body = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment...'}))
    class Meta:
        model = Comment
        fields = ('body',)

    def clean_body(self):
        body = self.cleaned_data.get('body')
        bad_words = BadWord.objects.all()
        results = list(map(lambda x: x.word, bad_words))
        body_list = body.split()
        bad_words_list = []
        for word in results:
            if word in body_list:
                bad_words_list.append(word)
        bad_words_string = ', '.join(bad_words_list)
        if len(bad_words_list) > 0:
            raise ValidationError("The body of a comment contain bad words " + bad_words_string)
        return body