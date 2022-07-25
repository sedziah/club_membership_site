# Django
from django import forms
from django.forms import ModelForm, widgets
from django.contrib.auth.forms import UserCreationForm

# Local Django
from .models import *
from .views import *


class DateInput(forms.DateInput):
    input_type = 'date'


class TimeInput(forms.TimeInput):
    input_type = 'time'


class CustomerProfilesForm(forms.ModelForm):

    class Meta:

        model = CustomerDetails
        fields = [
            'first_name',
            'last_name',
            'date_of_birth',
            'address',
            'hobbies',
            'national_id_type',
            'national_id',
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'},),
            'last_name': forms.TextInput(attrs={'class': 'form-control'},),
            'date_of_birth': DateInput(attrs={'class': 'form-control', },),
            'address': forms.TextInput(attrs={'class': 'form-control'},),
            'Hobbies': forms.TextInput(attrs={'class': 'form-control'},),
            'national_id': forms.TextInput(attrs={'class': 'form-control'},),
        }


class CustomerApprovalForm(forms.ModelForm):

    class Meta:

        model = CustomerDetails
        fields = ['customer_id', 'registration_status']

        widgets = {
            'customer_id': forms.TextInput(attrs={'class': 'form-control'},),
            'registration_status': forms.Select(attrs={'class': 'form-control'},),
        }


class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100)


class CustomerPaymentsForm(forms.ModelForm):

    class Meta:

        model = CustomerPayments
        fields = [
            'customer_id',
            'amount_paid',
            'payment_date'
        ]

        widgets = {
            'customer_id': forms.TextInput(attrs={'class': 'form-control'},),
            'amount_paid': forms.TextInput(attrs={'class': 'form-control', },),
            'payment_date': DateInput(attrs={'class': 'form-control', },),
        }


class CustomerReservationForm(forms.ModelForm):

    class Meta:

        model = CustomerReservations
        fields = ['facility', 'reservation_date', 'reservation_time']

        widgets = {
            'facility': forms.Select(attrs={'class': 'form-control'},),
            'reservation_date': DateInput(attrs={'class': 'form-control', },),
            'reservation_time': TimeInput(),
        }
