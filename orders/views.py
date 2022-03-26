from distutils import dist
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model

from rest_framework import viewsets

from .serializers import OrderSerializer, UserSerializer
from .models import Order



class UserListAPIView(viewsets.ModelViewSet):
    queryset = get_user_model().objects.order_by('username')
    serializer_class = UserSerializer

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.order_by('item')
    serializer_class = OrderSerializer
    
    def get_queryset(self):
        """
        Fetch all Orders, with filters
            a. By All orders
            b. By Nearby x kilometer
            c. By order status (Pending, ongoing, canceled , delivered)
        """
        queryset = Order.objects.all()

        # filter by location and radius
        location = self.request.query_params.get('location')
        if location:
            latitude,longitude,km = location.split(',')

            # radius in meters
            radius = float(km)*1000 
            user_location = Point(float(longitude), float(latitude), srid=4326)
            queryset = queryset.annotate(
                distance=Distance('location', user_location)
            ).filter(distance__lte=radius).order_by('distance')
        
        # filter by order status
        status = self.request.query_params.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset
