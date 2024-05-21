from django import forms
from products.models import *
from django.contrib.auth.forms import UserCreationForm

class CustomerRegistrationForm(UserCreationForm):
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    otchestvo = forms.CharField(max_length=30, label='Отчество (необязательно)')
    email = forms.CharField(max_length=30, required=True, label='Адрес электронной почты')
    phone_number = forms.CharField(max_length=20, required=True, label='Номер телефона')
    soglasie = forms.BooleanField(required=True, label='Согласен на обработку персональных данных')

    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + ('last_name', 'first_name', 'otchestvo', 'email', 'phone_number', 'soglasie')
