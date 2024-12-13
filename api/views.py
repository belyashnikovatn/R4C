from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.decorators import action
from django.utils import timezone
import pandas as pd

from robots.models import Robot
from api.serializers import RobotGetSerializer, RobotPostSerializer


class RobotViewSet(viewsets.ModelViewSet):
    queryset = Robot.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RobotGetSerializer
        return RobotPostSerializer

    @action(detail=False,)
    def download_summary(self, request):
        """Скачать Excel-файл со сводкой."""
        robots = Robot.objects.all().values('serial')
        df = pd.DataFrame(list(robots))
        # xlsx_data = create_excel()
        # response.write(xlsx_data)
        # response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename="summary_for.xlsx"'
        df.to_excel(response, index=False, engine='openpyxl')
        return response
