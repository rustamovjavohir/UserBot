from abc import ABC

from rest_framework import serializers
from staff.models import Bonus


class BonusSerializer(serializers.Serializer):
    document = serializers.CharField(max_length=250, allow_null=True)
    bonus = serializers.IntegerField(required=True)
    date = serializers.DateTimeField(allow_null=True)
    nomer = serializers.CharField(max_length=50)
    summa = serializers.IntegerField(allow_null=True)
    manager = serializers.CharField(max_length=250, allow_null=True)
    idmaneger = serializers.IntegerField(required=True)

