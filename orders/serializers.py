from django.contrib.auth import get_user_model
from rest_framework import serializers
from .pointfield import PointField
from .models import Order


User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username','password', 'first_name', 'mobile','user_type']
        write_only_fields = ('password',)
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class OrderSerializer(serializers.ModelSerializer):
    location = PointField()
    class Meta:
        model = Order
        fields = '__all__'

