"APIs for the exercise"

from rest_framework import viewsets
from . import serializers, models


class EmployeeModelViewSet(viewsets.ModelViewSet):  # pylint: disable=missing-class-docstring
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
