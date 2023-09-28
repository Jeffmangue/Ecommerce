from django.contrib import admin
from .models import ProductImagesModel, ProductsModel, CartModel
# Register your models here.
admin.site.register(ProductsModel)
admin.site.register(ProductImagesModel)
admin.site.register(CartModel)