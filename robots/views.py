from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers import RobotPostSerializer, RobotGetSerializer
from robots.models import Robot


class RobotRead(generics.ListAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'robots/read.html'

    def get(self, request):
        robots = Robot.objects.all()
        return Response({'robots': robots})


class RobotCreate(generics.CreateAPIView):
    serializer_class = RobotPostSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'robots/create.html'

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('robots:read')
        else:
            context = {'serializer': serializer}
            return Response(context, template_name=self.template_name)


class RobotEdit(generics.UpdateAPIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'robots/edit.html'

    def get(self, request, pk):
        robot = get_object_or_404(Robot, pk=pk)
        serializer = RobotPostSerializer(robot)
        return Response({'serializer': serializer, 'robot': robot})

    def post(self, request, pk, *args, **kwargs):
        robot = get_object_or_404(Robot, pk=pk)
        serializer = RobotPostSerializer(robot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('robots:read')
        else:
            context = {'serializer': serializer}
            return Response(context, template_name='robots/create.html')
            # robots = Robot.objects.all()
            # context = {'robots': robots}
            # return Response(context, template_name='robots/read.html')


class RobotDelete(APIView):
    renderer_classes = [TemplateHTMLRenderer]

    def get(self, request, pk):
        robot = get_object_or_404(Robot, pk=pk)
        context = {'pk': pk}
        robot.delete()
        return Response(context, template_name='robots/delete.html')
