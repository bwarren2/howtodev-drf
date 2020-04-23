from rest_framework import viewsets
from . import models
from . import serializers


class SeasonViewSet(viewsets.ModelViewSet):

    queryset = models.Season.objects.all()
    serializer_class = serializers.SeasonSerializer
