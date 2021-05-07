from django import forms
from .models import Group
from django.contrib.auth.models import User

class GroupModelForm(forms.ModelForm):
    class Meta:
        model = Group
        fields=('name','description', 'created_by')
        widgets = {'created_by': forms.HiddenInput()}
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(GroupModelForm, self).__init__(*args, **kwargs)
        self.fields['created_by']=  forms.ModelChoiceField(queryset=User.objects.filter(pk=user.id), required=False, initial=user.id)