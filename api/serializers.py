from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator


from robots.models import Robot


class RobotSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('__all__')
        model = Robot
