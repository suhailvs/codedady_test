
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from orders.views import OrderView, UserListAPIView, TakeOrderView
router = routers.DefaultRouter()

# core urls
router.register(r'users', UserListAPIView)
router.register(r'orders', OrderView)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-token-auth/', obtain_auth_token),
    path('take_order/', TakeOrderView.as_view()),
]
