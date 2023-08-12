from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Product, Collection, Review, Cart, CartItem, Customer, Order, OrderItem


class CollectionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id','title', 'products_count']
    products_count = serializers.IntegerField(read_only=True)

class SimpleProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']

class ProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)
    

class CartItemProductSerializers(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'unit_price']
    

class CartItemSerializers(serializers.ModelSerializer):
    product = CartItemProductSerializers()
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart_item:CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

class CartSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializers(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price']


class AddCartItemSerializers(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        return self.instance
    
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("There is no product with this id !")
        return value
        
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


class UpdateCartItemSerializers(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']
    

class CustomerSerializers(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Customer
        fields = ['id', 'user_id','phone', 'birth_date', 'membership']


class OrderItemSerializers(serializers.ModelSerializer):
    product = SimpleProductSerializers()
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'unit_price']


class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializers(many=True)
    class Meta:
        model = Order
        fields = ['id', 'customer', 'payment_status_summary', 'placed_at', 'items']


class CreateOrderSerializers(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def save(self, **kwargs):
        with transaction.atomic():
            cart_id = self.validated_data['cart_id']
            user_id = self.context['user_id']
            (customer, created) = Customer.objects.get_or_create(user_id = user_id)
            order = Order.objects.create(customer=customer)
            cart_items = CartItem.objects \
                .select_related('product').filter(cart_id = cart_id)
            order_items =[
                OrderItem(
                    order = order,
                    product = item.product,
                    unit_price = item.product.unit_price,
                    quantity = item.quantity,
                ) for item in cart_items
                ]
            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=user_id).delete()

            return order