from django.db import transaction
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from telegram import Bot
from config.settings import S_TOKEN
from api.serializers import BonusSerializer
import datetime
from pytz import timezone
from dateutil import parser
from staff.models import *

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
                            if int(i.ostatok.replace(",", "")) == 0:
                                continue
                            Leave.objects.create(full_name=i.full_name, month=i.month, year=i.year,
                                                 fine=int(i.ostatok.replace(",", "")))
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
    queryset = Bonus.objects.all()
    months = getMonthList()
    permission_classes = [IsAuthenticated]

    serializer_class = BonusSerializer

    def get_serializer(self, *args, **kwargs):
        return self.serializer_class(*args, **kwargs)

    def post(self, request):
        serializer = BonusSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            worker = Workers.objects.filter(telegram_id=serializer.data.get('idmaneger')).first()
            try:
                if worker:
                    date = datetime.datetime.strptime(serializer.data.get("date"), '%Y-%m-%dT%H:%M:%S%z')
                    bonus = serializer.data.get('bonus') // 10
                    bonus = Bonus.objects.create(full_name=worker, month=self.months[date.month - 1],
                                                 year=date.year, bonus=bonus, paid=0)
                    data = {
                        "success": True,
                        "status_code": 200,
                        "statusMessage": "Бонус успешно добавлен",
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
        return Response(status=200, data=data)
