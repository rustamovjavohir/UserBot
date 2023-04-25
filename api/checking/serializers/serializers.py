from rest_framework import serializers


class CheckingSerializer(serializers.Serializer):
    imageData = serializers.CharField()
