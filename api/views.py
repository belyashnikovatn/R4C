from django.contrib import messages
from io import BytesIO
import pandas as pd

from django.shortcuts import get_object_or_404, redirect
from django.db.models import Count
from django.http import HttpResponse
from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.renderers import TemplateHTMLRenderer, JSONRenderer
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.views import APIView

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




class RobotList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'robot_list.html'

    def get(self, request):
        queryset = Robot.objects.all()
        return Response({'robots': queryset})


class RobotDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def delete(self, request):
        robot = get_object_or_404(Robot, pk=pk)
        robot.delete()
        return Response({'robots': Robot.objects.all()}, template_name='robot_list.html')


class RobotDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'robot_detail.html'

    def get(self, request, pk):
        robot = get_object_or_404(Robot, pk=pk)
        serializer = RobotPostSerializer(robot)
        return Response({'serializer': serializer, 'robot': robot})

    # def delete(self, request, pk):
    #     robot = get_object_or_404(Robot, pk=pk)
    #     robot.delete()
    #     # serializer = RobotPostSerializer(robot)
    #     # return Response({'serializer': serializer, 'robot': robot})
    #     return Response({'robots': Robot.objects.all()}, template_name='robot_list.html')

    def post(self, request, pk):
        robot = get_object_or_404(Robot, pk=pk)
        serializer = RobotPostSerializer(robot, data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer, 'robot': robot})
        serializer.save()
        return Response({'robots': Robot.objects.all()}, template_name='robot_list.html')



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


class OrderViewSet(viewsets.ModelViewSet):
    """Вью для заказов: crud-операции."""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
