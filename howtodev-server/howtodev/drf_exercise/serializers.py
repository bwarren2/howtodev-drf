"Serializers."

from rest_framework import serializers
from drf_exercise import models


class TeamSerializer(serializers.ModelSerializer):  # pylint: disable=missing-class-docstring
    class Meta:  # pylint: disable=missing-class-docstring
        model = models.Team
        fields = ('name',)


class BaseSnackSerializer(serializers.ModelSerializer):  # pylint: disable=missing-class-docstring
    class Meta:  # pylint: disable=missing-class-docstring
        model = models.Snack
        fields = ('name', )


class BaseEmployeeSerializer(serializers.ModelSerializer):  # pylint: disable=missing-class-docstring
    class Meta:  # pylint: disable=missing-class-docstring
        model = models.Employee
        fields = ('name', )


class EmployeeSerializer(serializers.ModelSerializer):  # pylint: disable=missing-class-docstring
    snacks = BaseSnackSerializer(many=True, source='snack_set')

    class Meta:  # pylint: disable=missing-class-docstring
        model = models.Employee
        fields = ('name', 'snacks')


class SnackSerializer(serializers.ModelSerializer):  # pylint: disable=missing-class-docstring
    owner_data = BaseEmployeeSerializer(source='owner')

    class Meta:  # pylint: disable=missing-class-docstring
        model = models.Snack
        fields = ('name', 'owner', 'owner_data')
