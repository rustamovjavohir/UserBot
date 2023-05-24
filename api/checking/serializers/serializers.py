from rest_framework import serializers

from api.authorization.serializers.serializers import WorkerSerializers
from apps.checking.models import Timekeeping


class CheckingSerializer(serializers.Serializer):
    imageData = serializers.CharField()


class TimekeepingSerializer(serializers.ModelSerializer):
    # worker = WorkerSerializers(many=False)

    class Meta:
        model = Timekeeping
        fields = ['worker', 'date', 'check_in', 'check_out', 'created_at']
        read_only_fields = ['worker', 'date', 'check_in', 'check_out', 'created_at']
