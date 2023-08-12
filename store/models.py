from django.contrib import admin
from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4
# Create your models here.

class Promotion(models.Model):
    decription = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=2, decimal_places=2)
    def __str__(self):
        return self.decription

class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Product', on_delete=models.SET_NULL,blank=True, null=True, related_name='+')

    class Meta:
        ordering = ['title']
    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)]
        )
    inventory = models.IntegerField(
        validators=[MinValueValidator(1)]
    )
    last_update = models.DateTimeField(auto_now_add=True)
    collection = models.ForeignKey('Collection', on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion, blank=True)

    class Meta:
        ordering = ['title']

    def __str__(self) -> str:
        return self.title

class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD , 'Gold'),
    ]
    phone = models.CharField(max_length=15)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        permissions = [
            ('view_history', 'Can view history'),
        ]

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
    


class Order(models.Model):
    PENDING = 'P'
    COMPLETE = 'C'
    FAIL = 'F'
    PAYMENT_STATUS = [
        (PENDING, 'Pending'),
        (COMPLETE, 'Complete'),
        (FAIL, 'Failed'),
        
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status_summary = models.CharField(max_length=1, choices=PAYMENT_STATUS, default=PENDING)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)

    class Meta:
        permissions = [
            ('cencel_order', 'Can cencel order'),
        ]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.id


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]

    def __str__(self) -> str:
        return f"Product Name : {self.product}  ----  Quantity : {self.quantity}"
    
class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='review')
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name





    


