from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, help_text="Optional.", label="이름")
    last_name = forms.CharField(max_length=30, required=False, help_text="Optional.", label="성")
    username = forms.CharField(max_length=30, required=False, help_text="Optional.")
    email = forms.EmailField(max_length=254, help_text="Required. Inform a valid email address.")

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )