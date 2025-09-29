from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    employee_id = forms.CharField(max_length=20, required=True)
    department = forms.CharField(max_length=100, required=True)
    position = forms.CharField(max_length=100, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'employee_id', 
                 'department', 'position', 'phone_number', 'password1', 'password2')