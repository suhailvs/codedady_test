from django.contrib.gis.db import models
# Create your models here.

from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    USER_TYPE_CHOICES = (
      (0, 'admin'), 
      (1, 'shopowner'),
      (2, 'deliveryboy'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES,blank=False)
    mobile = models.PositiveBigIntegerField(blank=False)
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('canceled', 'Canceled'),
        ('delivered', 'Delivered'),
    )
    deliveryboy = models.OneToOneField('User',on_delete=models.SET_NULL, null=True)
    item = models.CharField(max_length=300)
    location = models.PointField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
