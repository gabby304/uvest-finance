from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth import get_user_model
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django_countries.fields import LazyTypedChoiceField, CountryField
from django_countries.widgets import LazySelect

class AccountCreationForm(UserCreationForm):
    
    phone_number = PhoneNumberField(
        widget=PhoneNumberPrefixWidget(
            initial='US',
            country_attrs={
                'class': 'form-control select2',
            },
            number_attrs={
                'id':'phone', 
                'class':'form-control', 
                'placeholder':'Phone Number', 
                'type': 'tel'
            },
        )
    )
    
    country = LazyTypedChoiceField(choices=CountryField(
        blank_label="Select Country").get_choices(), 
        widget=LazySelect(
            attrs={
            'class': 'form-control',
            'id':'country'
        }
    ))
    
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email', 'phone_number', 'country', 'gender', 'password1', 'password2')
        

class LoginForm(AuthenticationForm):
    pass


class AccountUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = (
                'email', 'phone_number',
                'first_name', 'last_name', 'address', 
                'city', 'zip_code', 'state',
                )
        
        
    
    

    
    
