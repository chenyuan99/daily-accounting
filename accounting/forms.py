from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from crispy_forms.helper import FormHelper

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()


class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class HistoryRecordForm(forms.ModelForm):
    class Meta:
        model = HistoryRecord
        # fields = '__all__'
        exclude = ['created_date', 'updated_date']


class TransferRecordForm(forms.ModelForm):
    class Meta:
        model = TransferRecord
        exclude = ['created_date', 'updated_date', 'currency']
