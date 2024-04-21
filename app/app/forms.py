from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=30)
