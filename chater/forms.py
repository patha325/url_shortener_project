from django import forms

class ChaterForm(forms.Form):
    message = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Type your message...',
        'class': 'form-control'
    }), max_length=500)