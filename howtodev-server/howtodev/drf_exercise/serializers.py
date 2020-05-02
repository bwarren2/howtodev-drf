"Serializers."

from rest_framework import serializers
from drf_exercise import models


class TeamSerializer(serializers.ModelSerializer):  # pylint: disable=missing-class-docstring
    class Meta:  # pylint: disable=missing-class-docstring
        model = models.Team
        fields = ('name',)


class SnackSerializer(serializers.ModelSerializer):  # pylint: disable=missing-class-docstring
    class Meta:  # pylint: disable=missing-class-docstring
        model = models.Snack
        fields = ('name',)


class EmployeeSerializer(serializers.ModelSerializer):  # pylint: disable=missing-class-docstring
    class Meta:  # pylint: disable=missing-class-docstring
        model = models.Employee
        fields = ('name',)
