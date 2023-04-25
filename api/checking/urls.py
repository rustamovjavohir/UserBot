from django.urls import path
from api.checking.views.views import CheckingPage, getIpAddress, SaveImage

urlpatterns = [
    path('checking/', CheckingPage.as_view(), name='checking'),
    path('save-image/', SaveImage.as_view(), name='save-image'),
    path('ip/', getIpAddress, name='get-ip'),
]
