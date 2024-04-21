from django import forms
from app import models


class LoginForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=30)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=30)


class SignupForm(forms.ModelForm):
    username = forms.CharField(min_length=3, max_length=30)
    email = forms.EmailField(min_length=6, max_length=30)
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = models.User
        fields = ['username', 'email', 'password']

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password != password_confirm:
            raise forms.ValidationError('Passwords do not match')

        return password_confirm

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        profile = models.Profile(user=user)

        if commit:
            user.save()
            profile.save()

        return user


class SettingsForm(forms.ModelForm):
    username = forms.CharField(min_length=3, max_length=30, required=False)
    email = forms.EmailField(min_length=6, max_length=30, required=False)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = models.User
        fields = ['username', 'email', 'avatar']

    def save(self, commit=True):
        user = super().save(commit=False)

        avatar = self.cleaned_data.get('avatar')
        if avatar:
            user.profile.avatar = avatar

        if commit:
            user.save()
            user.profile.save()

        return user
