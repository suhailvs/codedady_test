from distutils import dist
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.geos import Point
from django.contrib.auth import get_user_model
from django.db.models import Exists
from django.db.models import OuterRef

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework import viewsets

from .serializers import OrderSerializer, UserSerializer
from .models import Order



class UserListAPIView(viewsets.ModelViewSet):
    queryset = get_user_model().objects.order_by('username')
    serializer_class = UserSerializer

    def get_queryset(self):
        """
        Fetch Delivery boys with filters
            a. By name
            b. By mobile number
        """
        queryset = get_user_model().objects.filter(user_type=2)

        # filter by name
        name = self.request.query_params.get('name')
        if name:
            queryset=queryset.filter(first_name__icontains=name)
            
        # filter by mobile
        mobile = self.request.query_params.get('mobile')
        if mobile:
            queryset = queryset.filter(mobile__icontains=mobile)
        
        # filter by location and radius
        location = self.request.query_params.get('location')
        if location:
            latitude,longitude,km = location.split(',')

            # radius in meters
            radius = float(km)*1000 
            user_location = Point(float(longitude), float(latitude), srid=4326)
            queryset = queryset.filter(
                Exists(Order.objects.filter(
                    deliveryboy=OuterRef('pk')
                ))
            ).annotate(
                distance=Distance('order__location', user_location)
            ).filter(distance__lte=radius).order_by('distance')
        return queryset

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


class TakeOrderView(APIView):
    """
    View to take order by a delivery boy.

    * Requires token authentication.
    * Only admin users are able to access this view.
    """
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        order = Order.objects.get(id=request.data['orderid'])
        if order.deliveryboy:
            return Response('Order already assigned')
        
        if hasattr(request.user,'order') and request.user.order:
            return Response('User already has order')
        
        order.deliveryboy = request.user
        order.save()
        return Response('Order succussfully assigned.')




