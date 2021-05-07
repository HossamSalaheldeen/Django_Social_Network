from django import forms
from .views import Profile

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model  = Profile
        fields = ('first_name', 'last_name', 'bio' , 'country' ,'gender', 'date_of_birth','avatar')
