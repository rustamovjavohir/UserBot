# from django.contrib.gis.utils import GeoIP
from collections import OrderedDict

from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView, ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from telegram import Bot

from api.checking.permissions import SuperAdminPermission, AdminPermission
from api.staff.filters.filters import WorkerFilter
from api.staff.paginations.paginations import WorkerPagination
from api.utils import get_client_ip
from apps.staff.models import *
from config.settings import S_TOKEN, ALLOWED_IPS
from api.staff.serializers.serializers import BonusSerializer, WorkerSerializer
import datetime

bot = Bot(token=S_TOKEN)


def error_404(request, exception):
    return render(request, '404.html')


class RequestSalary(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = {
            "status": True,
            "method": 'GET',
            "description": "Method not allowed"
        }
        return Response(data=data, status=200)

    @transaction.atomic
    def post(self, request):
        bot.send_message(chat_id=779890968, text=request.data)
        if request.data.get('status') == "success":
            try:
                req = Request_price.objects.get(pk=request.data["id"], answer=False)
                workers = req.workers.all()

                if req.is_deleted:
                    workers = ITRequestPrice.objects.filter(secondId=request.data["id"], answer=False).first()
                    workers = workers.workers.all()
                    req.answer = True
                    req.save()
                    for i in workers:
                        try:
                            bot.send_message(chat_id=i.telegram_id, text="✅To`lov qabul qilindi")
                        except Exception as ex:
                            pass
                    return Response(status=200, data={"status": "ok"})
                else:
                    if not req.avans:
                        for i in workers:
                            if int(i.ostatok_1) == 0:
                                continue
                            Leave.objects.create(full_name=i.full_name, month=i.month, year=i.year,
                                                 fine=int(i.ostatok_1))
                        req.answer = True
                        req.save()
                        return Response(status=200, data={"status": "ok"})
                    else:
                        for i in workers:
                            Leave.objects.create(full_name=i.full_name, month=req.month, year=i.year, fine=req.price)
                            try:
                                bot.send_message(chat_id=i.full_name.telegram_id, text="✅To`lov qabul qilindi")
                            except Exception as ex:
                                pass
                        req.answer = True
                        req.save()
                        return Response(status=200, data={"status": "ok"})
            except Exception as ex:
                print(ex)
                return Response(status=400, data={"status": "error"})
        return Response(status=400, data={"status": "error"})


class BonusView(APIView):
    queryset = Bonus.objects.filter(is_deleted=False)
    months = getMonthList()
    permission_classes = [IsAuthenticated]
    ip_address = ALLOWED_IPS
    serializer_class = BonusSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def post(self, request):
        if get_client_ip(request) in self.ip_address:
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid(raise_exception=True):
                worker = Workers.objects.filter(telegram_id=serializer.data.get('idmaneger')).first()
                try:
                    if worker:
                        date = datetime.datetime.strptime(serializer.data.get("date"), '%Y-%m-%dT%H:%M:%S%z')
                        bonus = serializer.data.get('bonus')
                        # bonus = Bonus.objects.create(full_name=worker, month=self.months[date.month - 1],
                        #                              year=date.year,
                        #                              bonus_id=serializer.data.get('id'), bonus=bonus, paid=0)
                        bonus, created = Bonus.objects.update_or_create(full_name=worker,
                                                                        month=self.months[date.month - 1],
                                                                        year=date.year,
                                                                        bonus_id=serializer.data.get('id'),
                                                                        defaults={"bonus": bonus, "paid": 0})
                        if created:
                            data = {
                                "success": True,
                                "status_code": 200,
                                "statusMessage": "Бонус успешно добавлен",
                                "id": bonus.id,
                            }
                        else:
                            data = {
                                "success": True,
                                "status_code": 200,
                                "statusMessage": "Бонус успешно обновлен",
                                "id": bonus.id,
                            }
                    else:
                        data = {
                            "success": False,
                            "status_code": 404,
                            "statusMessage": "Сотрудник не найден",
                        }
                except Exception as ex:
                    data = {
                        "success": False,
                        "status_code": 404,
                        "statusMessage": ex.__str__(),
                    }
                    print(ex)
            else:
                data = {
                    "success": False,
                    "status_code": 400,
                    "statusMessage": "Поля не заполнены",
                }
        else:
            data = {
                "success": False,
                "status_code": 403,
                "statusMessage": f"Неверный IP-адреса ({get_client_ip(request)})",
            }
        return Response(status=200, data=data)

    def delete(self, request):
        if self.ip_address == get_client_ip(request):
            bonus_id = request.data.get('id')
            if bonus_id:
                if self.queryset.filter(bonus_id=bonus_id).exists():
                    self.queryset.filter(bonus_id=bonus_id).update(is_deleted=True)
                    data = {
                        "success": True,
                        "status_code": 200,
                        "statusMessage": "Бонус успешно удален",
                    }
                else:
                    data = {
                        "success": False,
                        "status_code": 404,
                        "statusMessage": "Бонус не найден",
                    }
            else:
                data = {
                    "success": False,
                    "status_code": 400,
                    "statusMessage": "Id Обязательное поле",
                }
        else:
            data = {
                "success": False,
                "status_code": 403,
                "statusMessage": f"Неверный IP-адреса ({get_client_ip(request)})",
            }

        return Response(status=200, data=data)


class WorkerAttributeView(APIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, ]
    queryset = Workers.objects.all()
    department_queryset = Department.objects.all()

    def get_department_list(self):
        user = self.request.user
        worker_user = user.workers_set.first()
        if worker_user.role == Workers.Role.USER:
            return []
        elif worker_user.role == Workers.Role.ADMIN:
            return list(
                self.department_queryset.filter(id=worker_user.department_id).order_by('name').values_list('name',
                                                                                                           flat=True))
        return list(self.department_queryset.order_by('name').values_list('name', flat=True))

    def get_department_json(self):
        return OrderedDict([
            ('name', 'department'),
            ('data', self.get_department_list())
        ])

    def get_job_list(self):
        user = self.request.user
        worker_user = user.workers_set.first()
        if worker_user.role == Workers.Role.USER:
            return []
        elif worker_user.role == Workers.Role.ADMIN:
            return list(self.queryset.filter(
                department_id=worker_user.department_id
            ).order_by('job').values_list('job', flat=True).distinct())
        return list(self.queryset.order_by('job').values_list('job', flat=True).distinct())

    def get_job_json(self):
        return OrderedDict([
            ('name', 'job'),
            ('data', self.get_job_list())
        ])

    def get_role_list(self):
        return Workers.Role.values

    def get_role_json(self):
        return OrderedDict([
            ('name', 'role'),
            ('data', self.get_role_list())
        ])

    @staticmethod
    def get_is_active_json():
        return OrderedDict([
            ('name', 'is_active'),
            ('data', [True, False])
        ])

    @staticmethod
    def get_in_office_json():
        return OrderedDict([
            ('name', 'in_office'),
            ('data', [True, False])
        ])

    @staticmethod
    def get_is_boss_json():
        return OrderedDict([
            ('name', 'is_boss'),
            ('data', [True, False])
        ])

    def get(self, request, *args, **kwargs):
        result = [
            self.get_department_json(),
            self.get_job_json(),
            self.get_role_json(),
            self.get_is_active_json(),
            self.get_in_office_json(),
            self.get_is_boss_json()
        ]

        return JsonResponse(OrderedDict([
            ('success', True),
            ("statusCode", 200),
            ('result', result)
        ]))


class WorkerListView(ListAPIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, AdminPermission]
    queryset = Workers.objects.filter(is_deleted=False).order_by('id')
    serializer_class = WorkerSerializer
    pagination_class = WorkerPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = WorkerFilter
    search_fields = ['full_name', 'department__name', 'phone', 'job']
    ordering_fields = ['id', 'department__name', 'job']

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        data = OrderedDict([
            ('success', False),
            ('statusCode', response.status_code),
            ('error', exc.detail),
            ('result', None)
        ])
        return Response(status=response.status_code, data=data)


class WorkerDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, AdminPermission]
    queryset = Workers.objects.filter(is_deleted=False).order_by('id')
    serializer_class = WorkerSerializer

    def get(self, request, *args, **kwargs):
        data = OrderedDict([
            ('success', True),
            ('statusCode', 200),
            ('error', None),
            ('result', self.get_serializer(self.get_object()).data)
        ])
        return Response(status=200, data=data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.user_delete()
        serializer = self.get_serializer(instance)
        data = OrderedDict([
            ('success', True),
            ('statusCode', 200),
            ('error', None),
            ('result', serializer.data)
        ])
        return Response(status=200, data=data)

    def handle_exception(self, exc):
        response = super().handle_exception(exc)
        error = exc.detail if hasattr(exc, "detail") else str(exc)
        data = OrderedDict([
            ('success', False),
            ('statusCode', response.status_code),
            ('error', error),
            ('result', None)
        ])
        return Response(status=response.status_code, data=data)
