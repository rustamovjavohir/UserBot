from django_filters.rest_framework import DjangoFilterBackend
from drf_excel.mixins import XLSXFileMixin
from rest_framework.filters import SearchFilter
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.authorization.serializers.serializers import WorkerSerializers
from api.checking.permissions import AdminPermission
from api.checking.serializers.serializers import TimekeepingSerializer
from api.files.utils import workers_2_xlsx, timekeeping_2_xlsx
from api.staff.filters.filters import WorkerFilter
from apps.checking.models import Timekeeping
from apps.staff.models import Workers


class ExportWorkersView(GenericAPIView):
    # authentication_classes = [JWTAuthentication, ]
    # permission_classes = [IsAuthenticated, AdminPermission]
    queryset = Workers.objects.all().order_by('department__name')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = WorkerSerializers
    search_fields = ['full_name', ]
    filterset_class = WorkerFilter

    def get(self, request):
        response = workers_2_xlsx(self.get_queryset())
        return response


class ExportTimekeepingView(GenericAPIView):
    # authentication_classes = [JWTAuthentication, ]
    # permission_classes = [IsAuthenticated, AdminPermission]
    queryset = Timekeeping.objects.all().order_by('-date', 'worker__department')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = TimekeepingSerializer
    # search_fields = ['full_name', ]
    # filterset_class = WorkerFilter

    def get(self, request):
        response = timekeeping_2_xlsx(self.get_queryset())
        return response

    # def get(self, request):
    #     queryset = self.filter_queryset(self.get_queryset())
    #     serializer = self.get_serializer(queryset, many=True)
    #     return Response(serializer.data)
