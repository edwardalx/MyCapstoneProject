# payments/forms.py
from django import forms

PROVIDER_CHOICES = [
    ('mtn', 'MTN'),
    ('vodafone', 'Vodafone'),
    ('airteltigo', 'AirtelTigo'),
]

class PaymentForm(forms.Form):
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label="Phone Number", max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}))
    provider = forms.ChoiceField(choices=PROVIDER_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    amount = forms.IntegerField(label="Amount (pesewas)", min_value=1, widget=forms.NumberInput(attrs={'class': 'form-control'}))
