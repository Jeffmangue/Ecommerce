from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ProductsModel(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    quantity = models.CharField(max_length=500, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    price = models.CharField(max_length=500, null=True, blank=True)
    category = models.CharField(max_length=500, null=True, blank=True)
    images = models.CharField(max_length=500, null=True, blank=True)
    availability = models.CharField(max_length=500, null=True, blank=True)
    sku = models.CharField(max_length=500, null=True, blank=True)
    created_date = models.CharField(max_length=500, null=True, blank=True)
    updated_date = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return str(self.name)
    

class ProductImagesModel(models.Model):
    product = models.ForeignKey(ProductsModel, on_delete=models.CASCADE, blank=True, null=True,  related_name='product_images')
    image = models.ImageField(null=True, blank=True, default="abc.jpg")
    def __str__(self):
        return str(self.product)
    
class CartModel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True,  related_name='cart_items')
    product_id = models.CharField(max_length=500, null=True, blank=True)
    quantity = models.CharField(max_length=500, null=True, blank=True)
    total = models.CharField(max_length=500, null=True, blank=True)
    order_date = models.DateField(max_length=500, null=True, blank=True)
    checked = models.BooleanField(default=False)
    checkout = models.BooleanField(default=False)
    ordered = models.CharField(max_length=500, null=True, blank=True)
    order_status = models.CharField(max_length=500, null=True, blank=True)
    cancelled = models.BooleanField(default=False)
    payment_method = models.CharField(max_length=500, null=True, blank=True)
    transaction_id = models.CharField(max_length=500, null=True, blank=True)
    shipment_tracking_information = models.CharField(max_length=500, null=True, blank=True)
    def __str__(self):
        return str(self.product_id)