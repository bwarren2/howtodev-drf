"APIs for the exercise"

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions, pagination
from . import serializers, models


class EmployeeModelViewSet(viewsets.ModelViewSet):  # pylint: disable=missing-class-docstring
    queryset = models.Employee.objects.all()
    serializer_class = serializers.EmployeeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['name', ]

