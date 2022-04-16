from django import forms
from core_app.models import *

class NewUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}), required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email_id = forms.CharField(required=True)
    password = forms.CharField(required=True)
    profile_picture = forms.FileField(required=True)
    
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'username', 'email_id', 'password', 'profile_picture', )


class NewAddressForm(forms.ModelForm):
    address_line1  = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    pincode = forms.CharField(required=True)
    
    class Meta:
        model = Address
        fields = ('address_line1', 'city', 'state', 'pincode', )