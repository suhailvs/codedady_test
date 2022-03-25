from django.contrib.gis.db import models
# Create your models here.
class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('ongoing', 'Ongoing'),
        ('canceled', 'Canceled'),
        ('delivered', 'Delivered'),
    )

    item = models.CharField(max_length=300)
    location = models.PointField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
