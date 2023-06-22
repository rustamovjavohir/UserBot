from django.urls import path

from api.staff.views.views import RequestSalary, BonusView, WorkerAttributeView, WorkerDetailView, WorkerListView

urlpatterns = [
    path("staffsalary/", RequestSalary.as_view()),
    path("bonus/", BonusView.as_view(), name='bonus'),
    path("workers/attribute/", WorkerAttributeView.as_view(), name='attribute'),
    path("workers/", WorkerListView.as_view(), name='workers-list'),
    path("workers/<int:pk>/", WorkerDetailView.as_view(), name='workers-detail'),
]
