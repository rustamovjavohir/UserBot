from abc import ABC

from rest_framework import serializers
from staff.models import Bonus


class BonusSerializer(serializers.Serializer):
    document = serializers.CharField(max_length=250, allow_null=True)
    id = serializers.CharField(max_length=250)
    date = serializers.DateTimeField(allow_null=True)
    nomer = serializers.CharField(max_length=50)
    bonus = serializers.IntegerField(required=True)
    summa = serializers.IntegerField(allow_null=True)
    currency: serializers.CharField(max_length=10, allow_null=True, allow_blank=True)
    store = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
    manager = serializers.CharField(max_length=250, allow_null=True)
    idmaneger = serializers.IntegerField(required=True)
    document_type = serializers.CharField(max_length=100, allow_null=True, allow_blank=True)
