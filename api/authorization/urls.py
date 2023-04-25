from django.urls import path
from api.authorization.views.views import LoginPage

urlpatterns = [
    path('', LoginPage, name='login'),
]
