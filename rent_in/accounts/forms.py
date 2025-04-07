from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import Tenant
from django.core.exceptions import ValidationError
import re
class TenantForm(UserCreationForm):
    username = forms.CharField(required=True, min_length=5, max_length=11,  label='Phone Number',
                widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control'})                       )
    id_image = forms.ImageField(required=False)
    first_name = forms.CharField(required=True, max_length=200)
    last_name = forms.CharField(required=True, max_length=200)
    email = forms.EmailField(required=True)  # Change to required=True

    class Meta:
        model = Tenant
        fields = ["username", "id_image", "first_name", "last_name", "email", "password1", "password2"]
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not re.match(r'^\d+$', username):  # regex to match only digits
            raise ValidationError("Username must contain numbers only.")
        return username

class TenantLoginForm(AuthenticationForm):
    username = forms.CharField(
         label='Phone Number',
        required=True,
        min_length=5,
        widget=forms.TextInput(attrs={'placeholder': 'Enter your phone number', 'class': 'form-control'})
    )
    class Meta:
        model = Tenant
        fields = ["username",'password']
    
class TenantUpdateForm(forms.Form):

    id_image = forms.ImageField(required=False)
    first_name = forms.CharField(required=True, max_length=200)
    last_name = forms.CharField(required=True, max_length=200)
    email = forms.EmailField(required=True)  # Change to required=True

    class Meta:
        model = Tenant
        fields = ["id_image", "first_name", "last_name", "email"]

