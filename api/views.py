from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.decorators import action
from django.utils import timezone
import pandas as pd
from io import BytesIO

from django.db.models import Count
from robots.models import Robot
from api.serializers import RobotGetSerializer, RobotPostSerializer


def get_models():
    """Return all models of robots"""
    return list(Robot.objects.values_list('model', flat=True)
                .distinct())


class RobotViewSet(viewsets.ModelViewSet):
    """View for robots-crud-operations + download xlsx-file."""
    queryset = Robot.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RobotGetSerializer
        return RobotPostSerializer

    @action(detail=False,)
    def download_summary(self, request):
        """Скачать Excel-файл со сводкой."""

        with BytesIO() as b:
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            for model in get_models():
                robots = Robot.objects.filter(model=model).values('model', 'version').annotate(dcount=Count('serial')).order_by()
                df = pd.DataFrame(data=list(robots))
                df.columns = ['Модель', 'Версия', 'Количество за неделю']
                df.to_excel(writer, index=False,
                            sheet_name=f'Модель робота {model}')
            writer.close()
            filename = 'test'
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
            return response
