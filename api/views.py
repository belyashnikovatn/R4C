from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, viewsets


from robots.models import Robot
from api.serializers import RobotSerializer


class RobotViewSet(viewsets.ModelViewSet):
    queryset = Robot.objects.all()
    serializer_class = RobotSerializer
