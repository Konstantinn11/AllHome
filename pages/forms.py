import datetime

from django import forms
from products.models import *
from django.contrib.auth.forms import UserCreationForm

class CustomerRegistrationForm(UserCreationForm):
    last_name = forms.CharField(max_length=30, required=True, label='Фамилия')
    first_name = forms.CharField(max_length=30, required=True, label='Имя')
    otchestvo = forms.CharField(max_length=30, label='Отчество')
    email = forms.CharField(max_length=30, required=True, label='Адрес электронной почты')
    phone_number = forms.CharField(max_length=20, required=True, label='Номер телефона')
    soglasie = forms.BooleanField(required=True, label='Согласен на обработку персональных данных')

    class Meta(UserCreationForm.Meta):
        model = Customer
        fields = UserCreationForm.Meta.fields + ('last_name', 'first_name', 'otchestvo', 'email', 'phone_number', 'soglasie')


class DatePickerForm(forms.Form):
    date = forms.DateField(required=False, label='Введите дату отчета',
                           widget=forms.DateInput(attrs={'max': datetime.date.today(), 'type': 'date'}))


class PeriodPickerForm(forms.Form):
    date1 = forms.DateField(required=False, label='Введите дату отчета с',
                           widget=forms.DateInput(attrs={'max': datetime.date.today(), 'type': 'date'}))
    date2 = forms.DateField(required=False, label='по',
                           widget=forms.DateInput(
                               attrs={'type': 'date'}))
