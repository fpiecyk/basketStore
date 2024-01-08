from django.contrib import admin
from basket.models import Category, Products, Order

# Register your models here.
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(Order)
