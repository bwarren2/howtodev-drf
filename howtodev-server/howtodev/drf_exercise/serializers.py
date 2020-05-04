"Serializers."

from rest_framework import serializers
from drf_exercise import models


class BaseTeamSerializer(serializers.ModelSerializer):  # pylint: disable=missing-class-docstring
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
    snacks = BaseSnackSerializer(many=True, source='snack_set', read_only=True)
    has_snacks = serializers.BooleanField()
    num_snacks = serializers.IntegerField()
    has_snacks_serializer_approach = serializers.SerializerMethodField()

    class Meta:  # pylint: disable=missing-class-docstring
        model = models.Employee
        fields = ('name', 'snacks', 'has_snacks', 'num_snacks', 'has_snacks_serializer_approach')

    def get_has_snacks_serializer_approach(self, obj):
        return len(obj.snack_set.all()) > 0


class SnackSerializer(serializers.ModelSerializer):  # pylint: disable=missing-class-docstring
    owner_data = BaseEmployeeSerializer(source='owner')

    class Meta:  # pylint: disable=missing-class-docstring
        model = models.Snack
        fields = ('name', 'owner', 'owner_data')


class NestedSnackSerializer(serializers.ModelSerializer):  # pylint: disable=missing-class-docstring

    class Meta:  # pylint: disable=missing-class-docstring
        model = models.Snack
        fields = ('name', 'owner')
