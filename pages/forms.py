from django import forms
from products.models import *
from django.contrib.auth.forms import UserCreationForm

class CustomerRegistrationForm(UserCreationForm):
    last_name = forms.CharField(max_length=30, label='Фамилия')
    first_name = forms.CharField(max_length=30, label='Имя')
    patronymic = forms.CharField(max_length=30, label='Отчество')
    email = forms.CharField(max_length=30, label='Адрес электронной почты')
    phone_number = forms.CharField(max_length=20, label='Номер телефона')

    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + ('last_name', 'first_name', 'patronymic', 'email', 'phone_number')
