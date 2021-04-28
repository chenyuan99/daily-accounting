import django_filters
from django_filters import DateFilter, CharFilter
from .models import *
from django import forms

class DateInput(forms.DateInput):
    input_type = 'date'

class currencyFilter(django_filters.FilterSet):
    class Meta:
        model = Currency
        fields = '__all__'


class accountFilter(django_filters.FilterSet):
    class Meta:
        model = Account
        fields = '__all__'


class categoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = '__all__'


class historyRecordFilter(django_filters.FilterSet):
    category = django_filters.ModelChoiceFilter(field_name='category', queryset=Category.objects.all(),label="分类&nbsp;&nbsp;",)
    account = django_filters.ModelChoiceFilter(field_name='account', queryset=Account.objects.all(),label="账户&nbsp;&nbsp;")
    from_date = django_filters.DateFilter(field_name='updated_date', lookup_expr='date__gte', widget=DateInput(attrs={'type': 'date'}),label="时间从&nbsp;&nbsp;")
    to_date = django_filters.DateFilter(field_name='updated_date', lookup_expr='date__lte', widget=DateInput(attrs={'type': 'date'}),label="到&nbsp;&nbsp;")
    class Meta:
        model = HistoryRecord
        fields = []
