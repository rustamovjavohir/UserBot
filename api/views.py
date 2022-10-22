from django.db import transaction
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from telegram import Bot
from config.settings import S_TOKEN

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
