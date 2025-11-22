from django import forms


class LoginForm(forms.Form):
    passport_serial = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())