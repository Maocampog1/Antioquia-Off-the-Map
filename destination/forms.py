from django import forms
from .models import TravelerPost, Review

class TravelerPostForm(forms.ModelForm):
    class Meta:
        model = TravelerPost
        fields = ['title', 'content', 'image', 'image2', 'image3', 'categories', 'municipality']
        labels = {
            'title': 'Título',
            'content': 'Contenido',
            'image': 'Imagen principal',
            'image2': 'Imagen secundaria',
            'image3': 'Imagen adicional',
            'categories': 'Categorías',
            'municipality': 'Municipio',
        }
        widgets = {
            'categories': forms.CheckboxSelectMultiple(), 
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-customGreen'}),
            'content': forms.Textarea(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-customGreen', 'rows': 4}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.HiddenInput(),
            'comment': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-customGreen',
                'rows': 4,
                'placeholder': 'Comparte tu experiencia...'
            }),
        }