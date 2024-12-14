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
    return list(Robot.objects.values_list('model', flat=True)
                .distinct())


class RobotViewSet(viewsets.ModelViewSet):
    queryset = Robot.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RobotGetSerializer
        return RobotPostSerializer

    @action(detail=False,)
    def download_summary(self, request):
        """Скачать Excel-файл со сводкой."""
        # # Второй вариант
        # df1 = pd.DataFrame(data = [1,2,3], columns = ['Numbers1'])
        # df2 = pd.DataFrame(data = [4,5,6], columns = ['Numbers2'])
        # excelBook = load_workbook('test.xlsx')
        # with pd.ExcelWriter('test.xlsx', engine='openpyxl') as writer:
        #     writer.book = excelBook
        #     writer.sheets = dict((ws.title, ws) for ws in excelBook.worksheets)
        #     df1.to_excel(writer, sheet_name='Tab1', index=False)
        #     df2.to_excel(writer, sheet_name='Tab2', index=False)
        #     writer.save()
        #     filename = 'test'
        #     content_type = 'application/vnd.ms-excel'
        #     response = HttpResponse(writer.getvalue(), content_type=content_type)
        #     response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
        #     return response
        
        # # Первый вариант 
        # robots = Robot.objects.values('model', 'version').annotate(dcount=Count('serial')).order_by()
        # df = pd.DataFrame(list(robots))
        # response = HttpResponse(writer, content_type='application/vnd.ms-excel')
        # response['Content-Disposition'] = 'attachment; filename="summary_for.xlsx"'
        # df.to_excel(response, sheet_name='Test', index=False, engine='openpyxl')
        # return response


        # df1 = pd.DataFrame(data = [1,2,3], columns = ['Numbers1'])
        # df2 = pd.DataFrame(data = [4,5,6], columns = ['Numbers2'])

        # with BytesIO() as b:
        #     # Use the StringIO object as the filehandle.
        #     writer = pd.ExcelWriter(b, engine='xlsxwriter')
        #     df1.to_excel(writer, sheet_name='Sheet1')
        #     df2.to_excel(writer, sheet_name='Sheet2')
        #     writer.close()
        #     filename = 'test'
        #     content_type = 'application/vnd.ms-excel'
        #     response = HttpResponse(b.getvalue(), content_type=content_type)
        #     response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
        #     return response
        

        
        # with BytesIO() as b:
        #     writer = pd.ExcelWriter(b, engine='xlsxwriter')
        #     # df = pd.DataFrame(data=[1,2,3], columns=['Numbers1'])
        #     # for model in list(Robot.objects.values_list('model', flat=True).distinct()):
        #     for model in get_models():
        #         robots = Robot.objects.filter(model=model).values('model', 'version').annotate(dcount=Count('serial')).order_by()
        #         df = pd.DataFrame(data=list(robots))
        #         df.to_excel(writer, sheet_name=model)
        # #     df1.to_excel(writer, sheet_name='Sheet1')
        # #     df2.to_excel(writer, sheet_name='Sheet2')
        #     writer.close()
        #     filename = 'test'
        #     content_type = 'application/vnd.ms-excel'
        #     response = HttpResponse(b.getvalue(), content_type=content_type)
        #     response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
        #     return response
        with BytesIO() as b:
            writer = pd.ExcelWriter(b, engine='xlsxwriter')
            # df = pd.DataFrame(data=[1,2,3], columns=['Numbers1'])
            # for model in list(Robot.objects.values_list('model', flat=True).distinct()):
            for model in get_models():
                robots = Robot.objects.filter(model=model).values('model', 'version').annotate(dcount=Count('serial')).order_by()
                df = pd.DataFrame(data=list(robots))
                df.columns = ['Модель', 'Версия', 'Количество за неделю']
                df.to_excel(writer, index=False,
                            sheet_name=f'Модель робота {model}')
        #     df1.to_excel(writer, sheet_name='Sheet1')
        #     df2.to_excel(writer, sheet_name='Sheet2')
            writer.close()
            filename = 'test'
            content_type = 'application/vnd.ms-excel'
            response = HttpResponse(b.getvalue(), content_type=content_type)
            response['Content-Disposition'] = 'attachment; filename="' + filename + '.xlsx"'
            return response

