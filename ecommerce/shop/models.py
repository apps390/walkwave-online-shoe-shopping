from django.db import models


# Create your models here.
class Category(models.Model):
    category_name = models.CharField(max_length=100)
    images = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.category_name


class Sub_category(models.Model):
    sub_category_name = models.CharField(max_length=100)
    uniquename = models.CharField(max_length=100, default="")
    images = models.ImageField(upload_to='sub_categories/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.uniquename


class Banner(models.Model):
    images = models.ImageField(upload_to="banners/", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Brand(models.Model):
    brandname = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    sub_categories = models.ManyToManyField(Sub_category)

    def __str__(self):
        return self.brandname
class Color(models.Model):
    color = models.CharField(max_length=200)
    categories = models.ManyToManyField(Category)
    sub_categories = models.ManyToManyField(Sub_category)
    def __str__(self):
        return self.color


class Product(models.Model):
    product_name = models.CharField(max_length=200)
    product_price = models.IntegerField()
    img1 = models.ImageField(upload_to='product/', null=True, blank=True)
    img2 = models.ImageField(upload_to='product/', null=True, blank=True)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    brand=models.ForeignKey(Brand,on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    Sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    description=models.TextField(default="lorem")
    def __str__(self):
        return self.product_name
class Size(models.Model):
    size=models.IntegerField()
    stock=models.DecimalField(max_digits=5,decimal_places=1)
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.product.product_name)
