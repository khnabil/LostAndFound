from django import forms
from .models import Item, ItemImage

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'date_reported', 'location', 'is_found']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe the item'}),
            'date_reported': forms.DateInput(attrs={'type': 'date'}),
            'name': forms.TextInput(attrs={'placeholder': 'Item name'}),
            'location': forms.TextInput(attrs={'placeholder': 'Where was it found/lost?'}),
        }

class MultiImageForm(forms.Form):
    images = forms.FileField(
        widget=forms.FileInput(attrs={
            'multiple': True,
            'accept': 'image/*'
        }),
        required=False,
        label="Upload Item Images"
    )
