from django import forms
from django.contrib.auth.forms import UserCreationForm
from . import models


class SignupForm(UserCreationForm):
    username = forms.CharField( max_length=15, required=True, help_text="Letters, digits and @/./+/-/_ only min 5 max 15 characters", min_length=5, widget=forms.TextInput(attrs={"autocomplete" : "off"}))

    class Meta(UserCreationForm.Meta):
        
        model = models.User
        fields = UserCreationForm.Meta.fields + ('shopName', 'mobileNumber', 'gstn', 'shopAddress')

class ShopProfileForm(forms.ModelForm):
    
    class Meta:
        model = models.User
        fields = ("username","shopName", "mobileNumber", "gstn", "email", "shopAddress")
