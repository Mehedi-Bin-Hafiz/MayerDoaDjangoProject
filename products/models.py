from django.db import models


class ProductGroup(models.Model):
    date = models.DateField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=80)
    def __str__(self):
        return self.name

class Products(models.Model):
    product_group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=80)
    price = models.FloatField(blank=True, null=True, max_length=80)
    def __str__(self):
        return self.name

class ProductStatus(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_out = models.CharField(blank=True, null=True, max_length=80)
    product_return = models.CharField(blank=True, null=True, max_length=80)
    final_price = models.FloatField(blank=True, null=True, max_length=80)
    def __str__(self):
        return str(self.product)

class DamageProduct(models.Model):
    product_group = models.ForeignKey(ProductGroup, on_delete=models.CASCADE)
    date = models.DateField(blank=True, null=True)
    name = models.CharField(blank=True, null=True, max_length=80)
    price = models.FloatField(blank=True, null=True, max_length=80)
    def __str__(self):
        return self.name
