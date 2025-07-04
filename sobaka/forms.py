from django import forms
from .models import Review, Human, NewsArticle

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
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'image1': forms.FileInput(attrs={'class': 'form-control'}),
            'image2': forms.FileInput(attrs={'class': 'form-control'}),
            'image3': forms.FileInput(attrs={'class': 'form-control'}),
            'image4': forms.FileInput(attrs={'class': 'form-control'}),
            'image5': forms.FileInput(attrs={'class': 'form-control'}),
            'available': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'height': forms.NumberInput(attrs={'class': 'form-control'}),
            'shoe_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'waist_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'bust_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'hip_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'eye_color': forms.TextInput(attrs={'class': 'form-control'}),
            'hair_color': forms.TextInput(attrs={'class': 'form-control'}),
        }

class NewsArticleForm(forms.ModelForm):
    class Meta:
        model = NewsArticle
        fields = ['title', 'image', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }

class ContactForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'}),
        help_text="Enter your email address."
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        help_text="Enter your measurements if contacting us about joining as a model."
    )
    picture = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text="Upload a headshot if contacting us about joining as a model."
    )