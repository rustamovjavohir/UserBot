from django.urls import path

from api.staff.views.views import *

urlpatterns = [
    path("staffsalary/", RequestSalary.as_view()),
    path("bonus/", BonusView.as_view(), name='bonus'),
]
