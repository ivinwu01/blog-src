# -*- coding: utf-8 -*-
# coding=utf-8
from django import forms


class ContactForm(forms.Form):
    username = forms.CharField(label='用户名', max_length=100)
    password = forms.CharField(label="""密　码""", widget=forms.PasswordInput())

    def clean_message(self):
        message = self.cleaned_data['username']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message
