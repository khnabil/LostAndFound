from django import forms
from .models import Item, ItemImage, Comment

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'date_reported', 'location', 'is_found']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'date_reported': forms.DateInput(attrs={'type': 'date'}),
        }

class ItemImageForm(forms.ModelForm):
    class Meta:
        model = ItemImage
        fields = ['image']



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 2,
                'placeholder': 'Write a comment...',
                'style': 'width: 100%; resize: none;'
            })
        }
