from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from .models import PamUsers


class PamUserForm(forms.ModelForm):
    class Meta:
        model = PamUsers
        fields = ['username', 'password', 'uid', 'gid']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()