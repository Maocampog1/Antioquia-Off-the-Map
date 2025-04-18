from django import forms
from .models import TravelerPost

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
        }
