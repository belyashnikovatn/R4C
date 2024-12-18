from io import BytesIO
import pandas as pd

from django.db.models import Count
from django.http import HttpResponse
from rest_framework import viewsets

from api.constants import PERIOD
from api.serializers import (
    CustomerSerializer,
    OrderSerializer,
    RobotGetSerializer,
    RobotPostSerializer,
)
from customers.models import Customer
from orders.models import Order
from robots.models import Robot


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


def download_summary(request):
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


class RobotViewSet(viewsets.ModelViewSet):
    """Вью для роботов: crud-операции + скачать Excel-файл."""
    queryset = Robot.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RobotGetSerializer
        return RobotPostSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    """Вью для покупателей: crud-операции."""
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """Вью для заказов: crud-операции."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
