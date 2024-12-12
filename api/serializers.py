from django.utils import timezone

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueTogetherValidator

from robots.models import Robot
from api.constants import (
    LETTERS,
    MODEL_LEN,
    VERSION_LEN
)


class RobotGetSerializer(serializers.ModelSerializer):
    """Роботы: GET."""

    class Meta:
        fields = ('__all__')
        model = Robot


class RobotPostSerializer(serializers.ModelSerializer):
    """Роботы: POST, валидация, предзаполнение."""
    model = serializers.CharField(required=True)
    version = serializers.CharField(required=True)
    created = serializers.DateTimeField(required=True)

    class Meta:
        fields = ('model', 'version', 'created')
        read_only_fields = ('serial',)
        model = Robot

    def validate(self, data):
        if 'model' not in data:
            raise serializers.ValidationError('Должна быть модель')
        if 'version' not in data:
            raise serializers.ValidationError('Должна быть версия')
        if 'created' not in data:
            raise serializers.ValidationError('Должна быть дата')
        return data

    def validate_model(self, data):
        if not all([char in LETTERS for char in data]):
            raise serializers.ValidationError(
                'В наименовании модели могут быть только символы'
            )
        if len(data) > MODEL_LEN:
            raise serializers.ValidationError(
                'Наименование модели не может быть больше 2-ух символов'
            )
        return data

    def validate_version(self, data):
        if not all([char in LETTERS for char in data]):
            raise serializers.ValidationError(
                'В наименовании версии могут быть только символы'
            )
        if len(data) > VERSION_LEN:
            raise serializers.ValidationError(
                'Наименование версии не может быть больше 2-ух символов'
            )
        return data

    def validate_created(self, data):
        if data > timezone.now():
            raise serializers.ValidationError(
                'Дата создания не может быть больше текущей'
            )
        return data

    def create(self, validated_data):
        serial = '-'.join([validated_data['model'], validated_data['version']])
        validated_data['serial'] = serial
        robot = Robot.objects.create(**validated_data)
        return robot

    def update(self, instance, validated_data):
        robot = instance
        robot.model = validated_data['model']
        robot.version = validated_data['version']
        robot.serial = '-'.join(
            [validated_data['model'], validated_data['version']])
        robot.save()
        return robot

    def to_representation(self, instance):
        return RobotGetSerializer(instance).data
