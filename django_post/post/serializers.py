from rest_framework import serializers
from .models import GeoModel


class GeoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeoModel
        fields = ['name', 'desc', 'type', 'poly', 'line', 'point', 'radius', 'id', 'points', 'place']
