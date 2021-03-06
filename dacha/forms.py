from django import forms
from . import models
from django.contrib.auth.models import User


class EmailMaterialForm(forms.Form):
    name = forms.CharField(max_length=255)
    to_email = forms.EmailField()
    comment = forms.CharField(required=False,
                              widget=forms.Textarea)


class MaterialForm(forms.ModelForm):
    class Meta:
        model = models.Material
        fields = ('title', 'body', 'material_type')


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)   # пароль звездочками


class CommentForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ('name', 'body')


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Pass',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Pass2',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):  # совпадение паролей
        cd = self. cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('bad password')
        return cd['password']


class UserEditForm(forms.ModelForm):  # форма для редактирования
    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ('birth', 'photo')
