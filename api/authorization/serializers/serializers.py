from collections import OrderedDict

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer, \
    TokenVerifySerializer

from api.checking.serializers.serializers import TimekeepingSerializer
from api.utils import get_current_date
from apps.staff.models import Workers, Department


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


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name']


class WorkerSerializers(serializers.ModelSerializer):
    department = serializers.CharField(source='department.name', required=False)
    job = serializers.CharField(required=False)
    # timekeeping_set = TimekeepingSerializer(many=True)
    timekeeping_set = serializers.SerializerMethodField(source='get_timekeeping_set')

    def get_timekeeping_set(self, obj):
        timekeeping = obj.timekeeping_set.filter(date=get_current_date().date()).first()
        if not timekeeping:
            return None
        serializer = TimekeepingSerializer(timekeeping, many=False)
        return serializer.data

    class Meta:
        model = Workers
        fields = ['id', 'full_name', 'department', 'job', 'phone', 'is_active', 'role', 'timekeeping_set']
        read_only_fields = ['id', 'department']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        if response['timekeeping_set']:
            response['date'] = response['timekeeping_set']['date']
            response['check_in'] = response['timekeeping_set']['check_in']
            response['check_out'] = response['timekeeping_set']['check_out']
            response['comment'] = response['timekeeping_set']['comment']
        else:
            response['date'] = None
            response['check_in'] = None
            response['check_out'] = None
            response['comment'] = None
        response.pop('timekeeping_set')
        return response

    def update(self, instance, validated_data):
        instance.full_name = validated_data.get('full_name', instance.full_name)
        instance.job = validated_data.get('job', instance.job)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.is_active = validated_data.get('is_active', instance.is_active)
        instance.role = validated_data.get('role', instance.role)
        instance.department = Department.objects.filter(
            name=validated_data.get('department', instance.department)).first()
        instance.save()
        return instance


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
        read_only_fields = ['id', 'is_superuser']

    def to_representation(self, instance):
        response = super().to_representation(instance)
        response['worker'] = None
        if response['workers_set']:
            response['worker'] = response['workers_set'][0]
        response.pop('workers_set')
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
        worker_data = validated_data.get('result', {}).get('workers_set', instance.workers_set)
        if worker_data:
            worker = Workers.objects.filter(id=instance.workers_set.first().id).first()
            worker.full_name = worker_data[0].get('full_name', worker.full_name)
            worker.phone = worker_data[0].get('phone', worker.phone)
            worker.save()
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


class ChangeUserPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, attrs):
        data = super().validate(attrs)
        response = OrderedDict([
            ('success', True),
            ('result', data),
            ('code', 'password_changed')
        ])
        return response

    def validate_confirm_password(self, value):
        if value != self.initial_data.get('new_password'):
            raise serializers.ValidationError('Password and confirm password does not match')
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('result', {}).get('new_password'))
        instance.save()
        return instance

    def to_representation(self, instance):
        return OrderedDict([
            ('success', True),
            ('code', 'password_changed')
        ])

    class Meta:
        model = User
        fields = ['new_password', 'confirm_password']
