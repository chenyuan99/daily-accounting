from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import ImageModel, TransferRecord, HistoryRecord, Account, Currency


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class PhotoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ImageModel
        fields = ['img', 'id']


class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Currency
        fields = []


class TransferRecordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = TransferRecord
        fields = ['from_account', 'to_account', 'time_of_occurrence', 'currency']


class AccountSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Account
        fields = ['name', 'amount', 'currency']
