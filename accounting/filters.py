import django_filters
from django_filters import DateFilter, CharFilter
from .models import *

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
    class Meta:
        model = HistoryRecord
        fields = '__all__'
