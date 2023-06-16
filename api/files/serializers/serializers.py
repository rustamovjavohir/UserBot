from rest_framework import serializers


class WorkersTimekeepingFile(serializers.Serializer):
    worker = serializers.CharField()

