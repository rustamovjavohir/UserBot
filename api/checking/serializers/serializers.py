from rest_framework import serializers
import locale
from apps.checking.models import Timekeeping


class CheckingSerializer(serializers.Serializer):
    imageData = serializers.CharField()


class TimekeepingSerializer(serializers.ModelSerializer):
    worker = serializers.CharField(source='worker.full_name', read_only=True)
    action = serializers.ChoiceField(choices=Timekeeping.ActionChoices, read_only=True)
    date = serializers.SerializerMethodField(source='get_date')

    class Meta:
        model = Timekeeping
        fields = ['id', 'worker', 'date', 'check_in', 'check_out', 'comment', 'action']
        read_only_fields = ['worker', 'date', 'check_in', 'check_out']

    def get_date(self, obj):
        return obj.date.strftime('%d-%m-%Y')


class TimekeepingDetailSerializer(serializers.ModelSerializer):
    worker = serializers.CharField(source='worker.full_name', read_only=True)
    date = serializers.SerializerMethodField(source='get_date')

    class Meta:
        model = Timekeeping
        fields = ['id', 'worker', 'date', 'check_in', 'check_out', 'comment']
        read_only_fields = ['id', 'worker', 'comment']

    def get_date(self, obj):
        return obj.date.strftime('%d-%m-%Y')


class CreateTimekeepingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Timekeeping
        fields = ['worker', 'date', 'check_in', 'check_out', 'comment']
        read_only_fields = ['id']
