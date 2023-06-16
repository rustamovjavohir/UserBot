from django.urls import path
from api.files.views.views import ExportWorkersView

urlpatterns = [
    path('workers/', ExportWorkersView.as_view(), name='export-workers'),
]
