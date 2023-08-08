from django.contrib import admin, messages
from django.db.models.query import QuerySet
from django.db.models import Count
from django.utils.html import format_html
from django.utils.http import urlencode
from django.urls import reverse
from .models import Promotion, Collection, Product, Customer, Order, OrderItem, Address, Cart, CartItem

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    low_val = '<10'
    ok_val = '>10'

    def lookups(self, request, model_admin):
        return [
            (self.low_val, 'Low'),
            (self.ok_val, 'Ok')
        ]
    def queryset(self, request, queryset: QuerySet):
        if self.value() == self.low_val:
            return queryset.filter(inventory__lt=10)
        return queryset.filter(inventory__gt=10)
    


        
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    search_fields = ['title__istartswith']
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug' : ['title']
    }
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price', 'inventory_status', 'collection']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 100

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'Ok'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f"{updated_count} product's were successfully updated.",
            messages.SUCCESS
        )
    
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders']
    autocomplete_fields = ['user']
    list_select_related = ['user']

    list_editable = ['membership']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    list_per_page = 100
    def orders(self, customer):
        url = (reverse('admin:store_order_changelist')
               + '?'
               + urlencode({
                   'customer__id' : str(customer.id)
               })
               )

        return format_html('<a href="{}">{}</a>',url, f"{customer.orders} orders")
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders = Count('order')
        )
    
class OrderItemInline(admin.TabularInline):
    autocomplete_fields = ['product']
    min_num = 1
    max_num = 10
    extra = 0
    model = OrderItem

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields = ['customer']
    list_display = ['id','placed_at', 'customer']
    inlines = [OrderItemInline]
    
    # list_select_related = ['customer']
    # def customer_title(self, order):
    #     return order.customer.email

@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title' , 'products_count']
    search_fields = ['title']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = (
            reverse('admin:store_product_changelist')
               + '?'
               + urlencode({
                  'collection__id' : str(collection.id) 
               }))
        return format_html('<a href="{}">{}</a>',url, f"{collection.products_count} products")
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count = Count('product')
        )
    
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id' , 'created_at']
    search_fields = ['id']

admin.site.register(CartItem)


