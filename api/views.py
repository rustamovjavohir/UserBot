from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from telegram import Bot
from config.settings import S_TOKEN

from staff.models import *

bot = Bot(token=S_TOKEN)


class RequestSalary(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.data["status"] == "success":
            try:
                req = Request_price.objects.get(pk=request.data["id"], answer=False)
                workers = req.workers.all()
                req.answer = True
                req.save()
                if not req.avans:
                    for i in workers:
                        if int(i.ostatok.replace(",", "")) == 0:
                            continue
                        Leave.objects.create(full_name=i.full_name, month=i.month, year=i.year,
                                             fine=int(i.ostatok.replace(",", "")))
                    return Response(status=200, data={"status": "ok"})
                else:
                    for i in workers:
                        Leave.objects.create(full_name=i.full_name, month=i.month, year=i.year, fine=req.price)
                        try:
                            bot.send_message(chat_id=i.full_name.telegram_id, text="✅To`lov qabul qilindi")
                        except Exception as ex:
                            print(ex)
                            pass
                    return Response(status=200, data={"status": "ok"})
            except Exception as ex:
                print(ex)
                return Response(status=400, data={"status": "error"})
        return Response(status=400, data={"status": "error"})
