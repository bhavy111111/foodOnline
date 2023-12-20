from .models import User
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())

    class Meta:
        model= User
        fields=['first_name','last_name','username','email','password']
    #whenever form is trigger , it using inbuilt pyhton function , in return it gives cleaned_data dictionary
    def clean(self):
        #super will override the cleaned_data
        cleaned_data = super(UserForm , self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password!=confirm_password:
            raise forms.ValidationError('Password does not match')