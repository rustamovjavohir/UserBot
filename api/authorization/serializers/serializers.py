from collections import OrderedDict

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, \
    TokenVerifySerializer
from apps.staff.models import Workers


class CustomObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(CustomObtainPairSerializer, cls).get_token(user)
        token['is_superuser'] = user.is_superuser
        return token

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['success'] = "Ok"
        return response

    def validate(self, attrs):
        data = super().validate(attrs)
        response = OrderedDict([
            ('success', True),
            ('result', data),
        ])
        return response


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = serializers.CharField()

    default_error_messages = {
        'bad_token': ('Token is invalid or expired')
    }

    def validate(self, attrs):
        data = super().validate(attrs)
        response = OrderedDict([
            ('success', True),
            ('result', data)
        ])
        return response


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class WorkerSerializers(serializers.ModelSerializer):
    class Meta:
        model = Workers
        fields = ['id', 'full_name', 'department', 'job', 'phone']


class WorkerTimekeepingSerializer(serializers.ModelSerializer):
    timekeeping_set = WorkerSerializers(many=False)

    class Meta:
        model = Workers
        fields = ['id', 'full_name', 'department', 'job', 'phone', "timekeeping_set"]


class UserProfilesSerializer(serializers.ModelSerializer):
    workers_set = WorkerSerializers(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'is_superuser', 'workers_set']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        data = OrderedDict([
            ('success', True),
            ('statusCode', 200),
            ('result', response)
        ])
        return data

    def validate(self, attrs):
        data = super().validate(attrs)
        response = OrderedDict([
            ('result', data)
        ])
        return response

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('result', {}).get('username', instance.username)
        instance.first_name = validated_data.get('result', {}).get('first_name', instance.first_name)
        instance.last_name = validated_data.get('result', {}).get('last_name', instance.last_name)
        instance.email = validated_data.get('result', {}).get('email', instance.email)
        instance.is_superuser = validated_data.get('result', {}).get('is_superuser', instance.is_superuser)
        instance.save()
        return instance

    def save(self, **kwargs):
        return super().save(**kwargs)


class VerifyTokenSerializer(TokenVerifySerializer):
    token = serializers.CharField()

    def validate(self, attrs):
        data = super().validate(attrs)
        response = OrderedDict([
            ('success', True),
            ('result', data),
            ('code', 'token_valid')
        ])
        return response
