from django.urls import path

from api.staff.views.views import *

from api.staff.urls import urlpatterns as staff_urls

urlpatterns = [
    # path("staffsalary/", RequestSalary.as_view()),
    # path("bonus/", BonusView.as_view(), name='bonus'),
]

urlpatterns += staff_urls
