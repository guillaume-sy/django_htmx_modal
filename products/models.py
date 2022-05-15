from django.db import models
from django.conf import settings
from django.utils import timezone


class Factory(models.Model):
    """Factory defines a location to store a product """
    factory_creating_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    factory_name = models.CharField(max_length=40)
    factory_reg_date = models.DateTimeField(default=timezone.now)
    factory_long_coordinates = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)
    factory_lat_coordinates = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)

    def __str__(self):
        return self.factory_name

    @property
    def owner(self):
        return self.factory_creating_user


class Product(models.Model):
    """Product defines a single element to be stored in a Factory """
    product_creating_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=40)
    product_reg_date = models.DateTimeField(default=timezone.now)
    product_factory_name = models.ForeignKey('Factory', on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name

    @property
    def owner(self):
        return self.product_creating_user
