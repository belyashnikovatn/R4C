from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework import viewsets
from rest_framework.decorators import action
import pandas as pd
from io import BytesIO

from django.db.models import Count
from robots.models import Robot
from customers.models import Customer
from api.serializers import (
    CustomerSerializer,
    RobotGetSerializer,
    RobotPostSerializer
)
from api.constants import PERIOD


def get_models(period=PERIOD) -> list[str]:
    """Возвращает новые за период модели."""
    new_robot_models = Robot.objects.filter(
        created__gte=period).values_list('model', flat=True).distinct()
    return list(new_robot_models)


def get_robots_by_model(model: str, period=PERIOD) -> list[str]:
    """Возвращает созданных за период роботов по модели."""
    new_robots = Robot.objects.filter(
        model=model, created__gte=period).values(
            'model', 'version').annotate(Count('serial')).order_by()
    return list(new_robots)


class RobotViewSet(viewsets.ModelViewSet):
    """Вью для роботов: crud-операции + скачать Excel-файл."""
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
                robots = get_robots_by_model(model)
                df = pd.DataFrame(data=list(robots))
                df.columns = ['Модель', 'Версия', 'Количество']
                df.to_excel(writer, index=False,
                            sheet_name=f'Модель робота {model}')
            writer.close()
            filename = f'Robots created since {PERIOD}'
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = (
                f'attachment; filename={filename}.xlsx')
            return response


class CustomerViewSet(viewsets.ModelViewSet):
    """Вью для покупателей: crud-операции."""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
