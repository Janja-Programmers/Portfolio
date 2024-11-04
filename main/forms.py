from django import forms

class PaymentForm(forms.Form):
    name = forms.CharField(label='Name', max_length=100)
    email = forms.EmailField(label='Email')
    phone_number = forms.CharField(label='Phone Number', max_length=15)
