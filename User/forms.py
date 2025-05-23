from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['class'] = 'form-control'

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['display_name', 'bio', 'profile_picture', 'birth_date', 'location']
        widgets = {
            'display_name': forms.TextInput(attrs={'class': 'form-control w-full text-left'}),
            'bio': forms.Textarea(attrs={'class': 'form-control w-full text-left', 'rows': 3}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control w-full text-left', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-control w-full text-left'}),
        }
