from rest_framework import serializers
from . import models


class SeasonSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Season
        fields = "__all__"
