from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=30)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    chosen = models.BooleanField(default=False)
    slider = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Image(models.Model):
    image = models.ImageField(upload_to='images')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.image.name


class Order(models.Model):
    address = models.CharField(max_length=250)
    phone = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    shipped = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity


