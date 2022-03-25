from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import OrderSerializer 
from .models import Order
class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.order_by('item')
    serializer_class = OrderSerializer
    
