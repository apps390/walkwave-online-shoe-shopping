from django.db import models
from django.contrib.auth.models import User
from shop.models import Product, Size


# Create your models here.

class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    date_added = models.DateTimeField(auto_now_add=True)

    def subtotal(self):
        return self.quantity * self.product.product_price


class Coupon(models.Model):
    coupon_name = models.CharField(max_length=30)
    discount = models.IntegerField()

    def __str__(self):
        return self.coupon_name


class Amount(models.Model):
    total_amnt = models.DecimalField(max_digits=15, decimal_places=3)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    name=models.CharField(max_length=20)
    address=models.CharField(max_length=60)
    phone_no=models.BigIntegerField()


