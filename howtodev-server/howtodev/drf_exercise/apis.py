"APIs for the exercise"

from django.db.models import Exists, Count, OuterRef, Subquery
from django.utils.decorators import method_decorator
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, permissions, pagination
from . import serializers, models


@method_decorator(
    name='list', decorator=swagger_auto_schema(
        responses={404: serializers.NotFoundSerializer}))
class EmployeeModelViewSet(viewsets.ModelViewSet):  # pylint: disable=missing-class-docstring
    """
    list: Foo
    create: Bar
    """
    queryset = models.Employee.objects.all().prefetch_related('snack_set').annotate(
        has_snacks=Exists(models.Snack.objects.filter(owner=OuterRef('pk'))),
        num_snacks=Count('snack')
    )
    serializer_class = serializers.EmployeeSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['name', ]


class SnackModelViewSet(viewsets.ModelViewSet):  # pylint: disable=missing-class-docstring
    queryset = models.Snack.objects.all().select_related('owner')
    serializer_class = serializers.SnackSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['name', ]


class SubSnackModelViewSet(viewsets.ModelViewSet):  # pylint: disable=missing-class-docstring
    queryset = models.Snack.objects.all()
    serializer_class = serializers.NestedSnackSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = pagination.LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ['name', ]

    def get_queryset(self):
        return models.Snack.objects.filter(
            # owner__pk=self.kwargs['employee_pk']
        ).select_related('owner')

    def get_serializer(self, *args, **kwargs):

        serializer_class = self.get_serializer_class()
        kwargs['context'] = self.get_serializer_context()
        if 'data' in kwargs:
            data = kwargs['data'].dict()
            data['owner'] = self.kwargs['employee_pk']
            kwargs['data'] = data
            return serializer_class(*args, **kwargs)
        else:
            return serializer_class(*args, **kwargs)
