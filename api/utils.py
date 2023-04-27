import base64
from datetime import datetime
from apps.checking.models import Workers
from PIL import Image
from io import BytesIO
from pytz import timezone
from django.core.files.base import ContentFile

from apps.staff.models import InfTech


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def base64_to_image(base64_string):
    img_data = base64.b64decode(base64_string)
    img = Image.open(BytesIO(img_data))
    return img


def save_cr_code(image_data, code_type="image"):
    unique_code = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    image_name = f"{code_type}_{unique_code}.png"
    data = ContentFile(base64.b64decode(image_data), name=f'{image_name}')
    return data


def get_worker_by_name(name, active=True):
    try:
        worker = Workers.objects.filter(full_name=name, active=active).first()
        if not worker:
            worker = InfTech.objects.filter(full_name=name, active=active).first()
        return worker
    except Workers.DoesNotExist:
        return None


def get_current_date():
    tz = timezone('Asia/Tashkent')
    return datetime.now(tz=tz)
