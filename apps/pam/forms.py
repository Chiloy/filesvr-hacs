from django import forms
from django.http import HttpResponse
from django.shortcuts import render
from .models import PamUsers, PamGroups, SftpPamUser


class UserPasswordHideForm(forms.ModelForm):
    class Meta:
        model = PamUsers
        fields = ['username', 'password', 'uid', 'homedir']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()