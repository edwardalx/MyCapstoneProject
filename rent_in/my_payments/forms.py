# payments/forms.py
from django import forms
from .models import Tenant, Property, Tenancy_Agreement

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
    
    tenancy_agreement = forms.ModelChoiceField(
        queryset=Tenancy_Agreement.objects.all(),
        label="Tenancy Agreement",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tenant = forms.ModelChoiceField(
        queryset=Tenant.objects.all(),
        label="Tenant",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    property = forms.ModelChoiceField(
        queryset=Property.objects.all(),
        label="Property",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
