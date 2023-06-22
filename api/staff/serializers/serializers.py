from collections import OrderedDict

from django.http import JsonResponse
from rest_framework import serializers
from rest_framework.response import Response

from apps.staff.models import Workers


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


class WorkerSerializer(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name', read_only=True)
    user = serializers.CharField(source='user.username', read_only=True, default=None)

    class Meta:
        model = Workers
        fields = ['id', 'full_name', 'department', 'job', 'phone', 'telegram_id', 'role', 'is_active', 'user']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        return response
