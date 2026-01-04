"""
Forms for the cases app.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Case


class UserRegistrationForm(UserCreationForm):
    """Custom registration form with additional fields."""
    
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your email'
    }))
    first_name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First name'
    }))
    last_name = forms.CharField(required=True, max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last name'
    }))
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })


class CaseReportForm(forms.ModelForm):
    """Form for reporting new cases."""
    
    class Meta:
        model = Case
        fields = ['case_type', 'place_spotted', 'needs', 'priority', 'image']
        widgets = {
            'case_type': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., Food Shortage, Malnutrition'
            }),
            'place_spotted': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter location details'
            }),
            'needs': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Describe the situation and needs in detail...'
            }),
            'priority': forms.Select(attrs={
                'class': 'form-select'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
        }


class CaseUpdateForm(forms.ModelForm):
    """Form for updating case status (Team/Admin only)."""
    
    class Meta:
        model = Case
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
