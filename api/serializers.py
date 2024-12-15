from django.utils import timezone
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField
from rest_framework.validators import UniqueValidator

from robots.models import Robot
from customers.models import Customer
from orders.models import Order
from api.constants import (
    EMAIL_LEN,
    LETTERS,
    MODEL_LEN,
    SERIAL_LEN,
    VERSION_LEN,
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


class CustomerSerializer(serializers.ModelSerializer):
    """Клиенты: валидация."""
    email = serializers.EmailField(
        required=True,
        max_length=EMAIL_LEN,
        validators=[UniqueValidator(queryset=Customer.objects.all())]
    )

    class Meta:
        fields = ('__all__')
        model = Customer


class OrderSerializer(serializers.ModelSerializer):
    """Заказы: валидация."""
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        required=True
    )
    robot_serial = serializers.CharField(
        max_length=SERIAL_LEN,
        required=True
    )

    class Meta:
        fields = ('__all__')
        model = Order

    def validate(self, data):
        if 'customer' not in data:
            raise serializers.ValidationError(
                'Укажите номер клиента'
            )
        if 'robot_serial' not in data:
            raise serializers.ValidationError(
                'Укажите серийный номер робота'
            )
        return data

    def validate_robot_serial(self, data):
        parts = data.split('-')
        if len(parts) != 2:
            raise serializers.ValidationError(
                'Неверно указан серийный номер'
            )
        model, version = parts

        if not all([char in LETTERS for char in model]):
            raise serializers.ValidationError(
                'В наименовании модели могут быть только символы'
            )
        if len(model) > MODEL_LEN:
            raise serializers.ValidationError(
                'Наименование модели не может быть больше 2-ух символов'
            )
        if not all([char in LETTERS for char in version]):
            raise serializers.ValidationError(
                'В наименовании версии могут быть только символы'
            )
        if len(version) > VERSION_LEN:
            raise serializers.ValidationError(
                'Наименование версии не может быть больше 2-ух символов'
            )
        return data
