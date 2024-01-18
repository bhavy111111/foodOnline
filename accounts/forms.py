from .models import User
from django import forms
from .models import UserProfile
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

class UserProfileForm(forms.ModelForm):
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start Typing..', 'required':'required'}))
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class':'btn btn-info'}))
    cover_photo = forms.ImageField(widget=forms.FileInput(attrs={'class':'btn btn-info'}))
    #latitude = forms.CharField()
    #Making ReadOnly Field 
    latitude =forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    longitude =forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))

    class Meta:
        model=UserProfile
        #fields=['profile_picture','cover_photo','address_line_1','address_line_2','country','state','city','pincode','latitude','longitutde']
        fields=['profile_picture','cover_photo','address','country','state','city','pincode','latitude','longitude']

class UserInfoForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','phone_number']

