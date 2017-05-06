from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model, authenticate

class LoginForm(forms.Form):
    email = forms.CharField(label='email')
    password = forms.CharField(label='password')

    def get_email(self):
        return self.email

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        self.email = cleaned_data.get("email")
        self.password = cleaned_data.get("password")
        if not User.objects.filter(email=self.email).exists():
            msg = "Email not registered"
            self.add_error('email', msg)
        elif self.email and self.password:
            user = authenticate(email=self.email, password=self.password)
            if user==None:
                msg = "Invalid Password"
                self.add_error('password', msg)


class RegisterForm(forms.Form):
    first_name = forms.CharField(label='first_name')
    email = forms.CharField(label='email')
    phone = forms.CharField(label='phone')

    def get_first_name(self):
        return self.first_name

    def get_email(self):
        return self.email

    def get_phone(self):
        return self.phone

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        self.first_name = cleaned_data.get('first_name')
        self.email = cleaned_data.get("email")
        self.phone = cleaned_data.get("phone")
        if User.objects.filter(email=self.email).exists():
            msg = "Email already registered"
            self.add_error('email', msg)



