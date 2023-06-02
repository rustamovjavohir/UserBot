from django.urls import path
from api.files.views.views import ExportWorkersView, ExportTimekeepingView

urlpatterns = [
    path('workers/', ExportWorkersView.as_view(), name='export-workers'),
    path('timekeeping/', ExportTimekeepingView.as_view(), name='export-timekeeping'),
]
