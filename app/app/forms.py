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


class AskForm(forms.ModelForm):
    tags = forms.CharField(required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    class Meta:
        model = models.Question
        fields = ['title', 'content']

    def clean_tags(self):
        return self.cleaned_data.get('tags').split()

    @staticmethod
    def add_tags_to_question(question, tags):
        for tag in tags:
            tag, created = models.Tag.objects.get_or_create(name=tag)
            question.tags.add(tag)

    def save(self, commit=True):
        question = models.Question(title=self.cleaned_data.get('title'),
                                   content=self.cleaned_data.get('content'))
        question.user = self.user

        if commit:
            question.save()
            AskForm.add_tags_to_question(question, self.cleaned_data.get('tags'))

        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = models.Answer
        fields = ['content']

    def __init__(self, user, question, *args, **kwargs):
        self.user = user
        self.question = question
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        answer = models.Answer(content=self.cleaned_data.get('content'))
        answer.user = self.user

        question = self.question
        question.answers_count += 1

        answer.question = question
        answer.is_correct = False

        if commit:
            answer.save()
            question.save()

        return answer
