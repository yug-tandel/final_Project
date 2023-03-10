from django.db import models
from seller.models import *

# Create your models here.
class BuyerDemo(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=250)
    pic = models.FileField(upload_to='buyer_profiles', default= 'avatar.jpg')
    
    def __str__(self) -> str:
        return self.email


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    buyer = models.ForeignKey(BuyerDemo, on_delete=models.CASCADE)

    def __str__ (self):
        return str(self.buyer)