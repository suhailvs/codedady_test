from rest_framework import serializers
from .pointfield import PointField
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    location = PointField()
    class Meta:
        model = Order
        fields = '__all__'
