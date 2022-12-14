from django.contrib import admin


from .models import ProductGroup, Products, ProductStatus, DamageProduct

admin.site.register(ProductGroup)
admin.site.register(Products)
admin.site.register(ProductStatus)
admin.site.register(DamageProduct)

