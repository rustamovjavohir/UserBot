import base64
from datetime import datetime

from PIL import Image
from io import BytesIO

from django.core.files.base import ContentFile


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


def get_current_date():
    return datetime.now().strftime('%Y-%m-%d')
