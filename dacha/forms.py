from django import forms
from . import models


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
    password = forms.CharField(widget=forms.PasswordInput)  #  пароль звездочками
