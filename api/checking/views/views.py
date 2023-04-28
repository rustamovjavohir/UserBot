import base64
import io

from django.http import HttpResponse, JsonResponse
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from telegram import InputMediaPhoto, InputFile

from api.utils import get_client_ip, base64_to_image, get_worker_by_name, get_current_date
from telegram.bot import Bot
from apps.checking.models import AllowedIPS, Timekeeping

from config import settings


class CheckingPage(TemplateView):
    template_name = 'intranet/checking.html'

    @staticmethod
    def get_allowed_ips():
        return AllowedIPS.getIPsList()

    def get_users(self, request):
        try:
            users = request.user.workers_set.first().department.workers_set.all().values_list('full_name', flat=True)
        except AttributeError:
            users = []
        return users

    def get(self, request, *args, **kwargs):
        if request.user.is_anonymous:
            return redirect('login')
        if get_client_ip(request) not in self.get_allowed_ips():
            # return render(request, '404.html')
            html = "<html><body><h1>IP address is %s.</h1></body></html>" % get_client_ip(request)
            return HttpResponse(html)

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
    permission_classes = [IsAuthenticated, ]
    bot = Bot(token=settings.S_TOKEN)

    def post(self, request, *args, **kwargs):
        if request.data.get('imageData') is not None:
            image_data = request.data.get('imageData')
            image_bytes = base64.b64decode(image_data.split('base64,')[1])
            image_file = InputFile(io.BytesIO(image_bytes), filename=f'image.png')
            caption = f"#{request.data.get('worker')}"
            self.bot.send_photo(chat_id=self.send_checking_id, photo=image_file, caption=caption)

            worker = get_worker_by_name(name=request.data.get('worker'))
            worker_time = Timekeeping.objects.get_or_create(worker=worker, date=get_current_date().date())[0]
            worker_time.setCheckIn()

            response = {
                'status': 'success',
                'message': 'Image processed successfully',
                'worker': request.data.get('worker')
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
