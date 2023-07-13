import base64
import io
from collections import OrderedDict

from django.core.exceptions import BadRequest
from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from telegram import InputMediaPhoto, InputFile

from api.authorization.serializers.serializers import WorkerSerializers
from api.checking.filters.filters import TimekeepingFilter
from api.checking.mixins import IsRadiusMixin
from api.checking.paginations.paginations import TimekeepingPagination
from api.checking.permissions import RadiusPermission, AdminPermission, SuperAdminPermission
from api.checking.serializers.serializers import TimekeepingSerializer, TimekeepingDetailSerializer, \
    CreateTimekeepingSerializer
from api.staff.filters.filters import WorkerFilter
from api.staff.paginations.paginations import WorkerPagination
from api.utils import get_client_ip, base64_to_image, get_worker_by_name, get_current_date
from telegram.bot import Bot
from apps.checking.models import AllowedIPS, Timekeeping
from apps.staff.models import Workers, Department

from config import settings


class CheckingPage(IsRadiusMixin, TemplateView):
    template_name = 'intranet/checking.html'

    @staticmethod
    def get_allowed_ips():
        return AllowedIPS.getIPsList()

    def get_users(self, request):
        try:
            users = request.user.workers_set.first().department.workers_set.all() \
                .filter(is_deleted=False).values_list('full_name', flat=True)
        except AttributeError:
            users = []
        return users

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('login')

        context = {
            'message': 'Hello World',
            'ip': get_client_ip(request),
            'username': request.user.username,
            'user': request.user,
            'users': self.get_users(request)
        }
        return render(request, self.template_name, context=context)


def getIpAddress(request):
    html = "<html><body><h1>IP address is %s.</h1></body></html>" % get_client_ip(request)
    return HttpResponse(html)


class SaveImage(APIView):
    send_checking_id = settings.SEND_CHECKING_ID
    authentication_classes = [SessionAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    bot = Bot(token=settings.S_TOKEN)

    def post(self, request, *args, **kwargs):
        if request.data.get('imageData') is not None:
            image_data = request.data.get('imageData')
            image_bytes = base64.b64decode(image_data.split('base64,')[1])
            image_file = InputFile(io.BytesIO(image_bytes), filename=f'image.png')
            worker = get_worker_by_name(name=request.data.get('worker'))
            comment = request.data.get('comment', None)
            worker_department = worker.department.name.replace(' ', '_')
            worker_name = worker.full_name.replace(' ', '_')
            caption = f"#{worker_department} \n#{worker_name}"
            if comment:
                caption += f"\n{comment}"
            self.bot.send_photo(chat_id=self.send_checking_id, photo=image_file, caption=caption)

            worker_time = Timekeeping.objects.get_or_create(worker=worker, date=get_current_date().date())[0]
            worker_time.setCheckInOrOut()
            response = {
                'status': 'success',
                'message': 'Image processed successfully',
                'worker': request.data.get('worker'),
                'comment': request.data.get('comment'),
            }
            return JsonResponse(response, status=200)

        return JsonResponse({'status': 'error', 'message': 'Image not processed'}, status=400)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        response.data['success'] = False
        response.data['statusCode'] = exc.status_code
        response.data['code'] = exc.default_code
        response.data['message'] = exc.detail
        response.data['result'] = None
        response.status_code = status.HTTP_200_OK
        response.data.pop('detail')

        return response


class UserTimekeepingView(ListAPIView):
    serializer_class = TimekeepingSerializer
    permission_classes = [IsAuthenticated]
    queryset = Timekeeping.objects.all().filter(is_deleted=False)
    worker_serializer_class = WorkerSerializers
    pagination_class = TimekeepingPagination

    def get_queryset(self):
        qs = super().get_queryset().filter(worker=self.request.user.workers_set.first())
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        worker_serializer = self.worker_serializer_class(self.request.user.workers_set.first())
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'worker': worker_serializer.data, 'timekeeping': serializer.data})


class SetTimekeepingView(GenericAPIView):
    serializer_class = TimekeepingSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def post(self, request, *args, **kwargs):
        worker = request.user.workers_set.first()
        comment = request.data.get('comment', None)
        action = request.data.get('action', None)
        worker_time = Timekeeping.objects.get_or_create(worker=worker, date=get_current_date().date())[0]
        if action == Timekeeping.ActionChoices.CHECK_IN:
            worker_time.setCheckIn()
        elif action == Timekeeping.ActionChoices.CHECK_OUT:
            worker_time.setCheckOutByApi()
        else:
            worker_time.setCheckInOrOut()
        if comment:
            old_comment = worker_time.comment if worker_time.comment else ""
            worker_time.comment = old_comment + " " + comment + ","
            worker_time.save()
        serializer = self.get_serializer(worker_time)
        response = OrderedDict([
            ('success', True),
            ("statusCode", 200),
            ("result", serializer.data),
        ])
        return JsonResponse(response, status=200)


class WorkerTimekeepingView(ListAPIView):
    serializer_class = TimekeepingSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, AdminPermission]
    queryset = Timekeeping.objects.all().filter(is_deleted=False)
    pagination_class = TimekeepingPagination

    def get_queryset(self):
        qs = super().get_queryset().filter(worker__id=self.kwargs.get('pk'))
        return qs

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        worker = Workers.objects.filter(id=self.kwargs.get('pk')).first()
        if worker is None:
            raise NotFound('Worker not found')
        worker_serializer = WorkerSerializers(worker)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({'worker': worker_serializer.data, 'timekeeping': serializer.data})


class WorkersDailyTimekeepingView(ListAPIView):
    serializer_class = WorkerSerializers
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, AdminPermission]
    queryset = Workers.objects.all().order_by('department__name', 'id').filter(is_deleted=False)
    pagination_class = WorkerPagination
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['full_name', ]
    filterset_class = WorkerFilter

    def get_queryset(self):
        if self.request.user.workers_set.first().role == Workers.Role.SUPER_ADMIN:
            return super().get_queryset()
        return super().get_queryset().filter(department__id=self.request.user.workers_set.first().department.id)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)


class DetailTimekeepingView(RetrieveUpdateAPIView):
    serializer_class = TimekeepingDetailSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, SuperAdminPermission]
    queryset = Timekeeping.objects.all().filter(is_deleted=False)

    def get_object(self):
        obj = super().get_object()
        return obj

    def handle_exception(self, exc):
        if isinstance(exc, PermissionDenied):
            data = OrderedDict([
                ('success', False),
                ("statusCode", 403),
                ("message", exc.detail),
                ("result", None),
            ])
            return JsonResponse(data, status=403)
        return super().handle_exception(exc)


class CreateTimekeepingView(GenericAPIView):
    serializer_class = CreateTimekeepingSerializer
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, AdminPermission]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        response = OrderedDict([
            ('success', True),
            ("statusCode", 200),
            ("message", "Create timekeeping success"),
            ("result", serializer.data),
        ])
        return JsonResponse(response, status=200)

    def handle_exception(self, exc):
        if isinstance(exc, BadRequest):
            data = OrderedDict([
                ('success', False),
                ("statusCode", 400),
                ("message", str(exc)),
                ("result", None),
            ])
            return JsonResponse(data, status=400)
        return super().handle_exception(exc)
