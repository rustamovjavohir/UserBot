from django.urls import path
from api.files.views.views import ExportWorkersView, ExportWorkDayTableView

urlpatterns = [
    path('workers/', ExportWorkersView.as_view(), name='export-workers'),
    path('workday-table/', ExportWorkDayTableView.as_view(), name='export-workday-table'),
]
