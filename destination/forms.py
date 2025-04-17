from django import forms
from .models import TravelerPost

class TravelerPostForm(forms.ModelForm):
    class Meta:
        model = TravelerPost
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea'}),
        }
