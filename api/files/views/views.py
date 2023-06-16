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
from api.files.utils import workers_2_xlsx
from api.staff.filters.filters import WorkerFilter
from apps.checking.models import Timekeeping
from apps.staff.models import Workers


class ExportWorkersView(GenericAPIView):
    authentication_classes = [JWTAuthentication, ]
    permission_classes = [IsAuthenticated, AdminPermission]
    queryset = Workers.objects.all().order_by('department__name')
    filter_backends = [DjangoFilterBackend, SearchFilter]
    serializer_class = WorkerSerializers
    search_fields = ['full_name', ]
    filterset_class = WorkerFilter

    def post(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        response = workers_2_xlsx(queryset, start_date, end_date)
        return response

    def get(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        response = workers_2_xlsx(queryset, start_date, end_date)
        return response

    # def post(self, request):
    #     # response = workers_2_xlsx(self.get_queryset())
    #     queryset = self.filter_queryset(self.get_queryset())
    #     start_date = request.query_params.get('start_date', None)
    #     end_date = request.query_params.get('end_date', None)
    #     serializer = self.serializer_class(queryset, many=True)
    #     return Response(serializer.data)
