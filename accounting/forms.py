from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, HTML
from decimal import Decimal


class BaseForm(forms.ModelForm):
    """Base form class with common functionality."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-loading-button'
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            if isinstance(field, forms.DateTimeField):
                field.widget.attrs.update({'class': 'form-control datepicker'})
            if isinstance(field, forms.DecimalField):
                field.widget.attrs.update({
                    'class': 'form-control currency-input',
                    'step': '0.01',
                    'min': '0'
                })


class UploadFileForm(BaseForm):
    """Form for file uploads."""
    title = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'placeholder': 'Enter file title'})
    )
    file = forms.FileField(
        widget=forms.FileInput(attrs={'class': 'form-control-file'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            'title',
            'file',
            Submit('submit', 'Upload', css_class='btn btn-primary mt-3')
        )


class NewUserForm(UserCreationForm):
    """Enhanced user registration form."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'Enter your email'})
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-loading-button'
        self.helper.layout = Layout(
            'username',
            'email',
            'password1',
            'password2',
            Submit('submit', 'Register', css_class='btn btn-primary mt-3')
        )
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class HistoryRecordForm(BaseForm):
    """Form for recording financial history."""
    
    class Meta:
        model = HistoryRecord
        exclude = ['created_date', 'updated_date']
        widgets = {
            'time_of_occurrence': forms.DateTimeInput(
                attrs={'class': 'form-control datepicker'}
            ),
            'comment': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Enter any additional notes'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('account', css_class='col-md-6'),
                Column('amount', css_class='col-md-6'),
            ),
            Row(
                Column('category', css_class='col-md-6'),
                Column('sub_category', css_class='col-md-6'),
            ),
            'time_of_occurrence',
            'comment',
            HTML('<div class="form-group mt-3">'),
            Submit('submit', 'Save Record', css_class='btn btn-primary'),
            HTML('</div>')
        )

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount and amount <= Decimal('0'):
            raise forms.ValidationError("Amount must be greater than zero")
        return amount


class TransferRecordForm(BaseForm):
    """Form for recording transfers between accounts."""
    
    class Meta:
        model = TransferRecord
        exclude = ['created_date', 'updated_date', 'currency']
        widgets = {
            'time_of_occurrence': forms.DateTimeInput(
                attrs={'class': 'form-control datepicker'}
            ),
            'comment': forms.Textarea(
                attrs={'rows': 3, 'placeholder': 'Enter transfer details'}
            )
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper.layout = Layout(
            Row(
                Column('from_account', css_class='col-md-6'),
                Column('to_account', css_class='col-md-6'),
            ),
            Row(
                Column('amount', css_class='col-md-6'),
                Column('time_of_occurrence', css_class='col-md-6'),
            ),
            'comment',
            HTML('<div class="form-group mt-3">'),
            Submit('submit', 'Transfer', css_class='btn btn-primary'),
            HTML('</div>')
        )

    def clean(self):
        cleaned_data = super().clean()
        from_account = cleaned_data.get('from_account')
        to_account = cleaned_data.get('to_account')
        amount = cleaned_data.get('amount')

        if from_account and to_account and from_account == to_account:
            raise forms.ValidationError("Cannot transfer to the same account")

        if amount and amount <= Decimal('0'):
            raise forms.ValidationError("Transfer amount must be greater than zero")

        if from_account and amount and amount > from_account.amount:
            raise forms.ValidationError("Insufficient funds in the source account")
