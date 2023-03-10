from django.db import models

# Create your models here.

class Seller(models.Model):
    full_name = models.CharField(max_length=50)
    mobile = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=30)
    gst_no = models.CharField(max_length=14, null=True, blank=True)

    def __str__(self):
        return self.full_name

class Product(models.Model):
    product_name = models.CharField(max_length=150)
    des = models.CharField(max_length = 250)
    price = models.DecimalField(max_digits=10, decimal_places=3,default=500)
    pic = models.FileField(upload_to='product_images', default='pro_def_img.jpg')
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name
