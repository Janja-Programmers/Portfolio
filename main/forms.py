from django import forms

class PaymentForm(forms.Form):
    name = forms.CharField(
        label='Name', 
        max_length=100, 
        widget=forms.TextInput(attrs={'placeholder': 'Your Full Name'})
    )
    email = forms.EmailField(
        label='Email', 
        widget=forms.EmailInput(attrs={'placeholder': 'you@example.com'})
    )
    phone_number = forms.CharField(
        label='Mpesa Number', 
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': '0794933942'})
    )
