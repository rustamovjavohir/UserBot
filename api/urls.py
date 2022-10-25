from django.urls import path

from api.views import *

urlpatterns = [
    path("staffsalary/", RequestSalary.as_view()),
    path("bonus/", BonusView.as_view(), name='bonus'),
]
