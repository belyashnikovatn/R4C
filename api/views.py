from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets


from robots.models import Robot
from api.serializers import RobotGetSerializer, RobotPostSerializer


class RobotViewSet(viewsets.ModelViewSet):
    queryset = Robot.objects.all()

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return RobotGetSerializer
        return RobotPostSerializer
