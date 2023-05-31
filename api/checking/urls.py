from django.urls import path
from api.checking.views.views import CheckingPage, getIpAddress, SaveImage, UserTimekeepingView, SetTimekeepingView, \
    WorkerTimekeepingView, WorkersDailyTimekeepingView

urlpatterns = [
    path('checking/', CheckingPage.as_view(), name='checking'),
    path('save-image/', SaveImage.as_view(), name='save-image'),
    path('ip/', getIpAddress, name='get-ip'),
    path('timekeeping/profile', UserTimekeepingView.as_view(), name='timekeeping'),
    path('timekeeping/profile/<int:pk>', WorkerTimekeepingView.as_view(), name='profile-timekeeping'),
    path('timekeeping/workers', WorkersDailyTimekeepingView.as_view(), name='workers-timekeeping'),
    path('timekeeping/set-time', SetTimekeepingView.as_view(), name='set-timekeeping'),

]
