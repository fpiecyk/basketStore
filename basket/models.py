from django.db import models
from authManager.models import CustomUser

class Category(models.Model):
    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=50)

    @staticmethod
    def get_all_categories():
        return Category.objects.all()

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=60)
    price= models.IntegerField()
    category= models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    description= models.CharField(max_length=250, blank=True, null= True)
    image= models.ImageField(upload_to='uploads/', blank=True, null=True)

    def __str__(self):
        return f'{self.name} | {self.price} | {self.category}'


    @staticmethod
    def get_products_by_id(ids):
        return Products.objects.filter(category_id__in=ids)
    @staticmethod
    def get_all_products():
        return Products.objects.all()

    @staticmethod
    def get_all_products_by_category_id(category_id):
        if category_id:
            return Products.objects.filter(category=category_id)
        else:
            return Products.get_all_products()


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=1)
    price = models.IntegerField(default=0)
    address = models.CharField(max_length=50, blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def place_order(self):
        # Calculate the total price and set it to the price field
        total_price = sum(item.total_price for item in self.orderitem_set.all())
        self.price = total_price
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')

    def get_total_price(self):
        return sum(item.total_price for item in self.orderitem_set.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.IntegerField()


class WishList(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    added = models.DateTimeField(auto_now_add=True)




