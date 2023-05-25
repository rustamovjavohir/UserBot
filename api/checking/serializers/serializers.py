from rest_framework import serializers

from apps.checking.models import Timekeeping


class CheckingSerializer(serializers.Serializer):
    imageData = serializers.CharField()


class TimekeepingSerializer(serializers.ModelSerializer):
    worker = serializers.CharField(source='worker.full_name', read_only=True)

    class Meta:
        model = Timekeeping
        fields = ['worker', 'date', 'check_in', 'check_out', 'comment']
        read_only_fields = ['worker', 'date', 'check_in', 'check_out']
