from django import forms
from .models import Review, Human

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(choices=[(i, i) for i in range(1, 6)]),
            'comment': forms.Textarea(attrs={'rows': 3}),
        }

class HumanForm(forms.ModelForm):
    class Meta:
        model = Human
        fields = ['name', 'category', 'price', 'image1', 'image2', 'image3', 'image4', 'image5', 'available', 'height', 'shoe_size', 'waist_size', 'bust_size', 'hip_size', 'eye_color', 'hair_color']