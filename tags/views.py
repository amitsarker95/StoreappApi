from django.shortcuts import render
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from store.models import Product, Collection, Order, OrderItem
from .models import TaggedItem


def query(request):
    content = TaggedItem.objects.get_tags_for(Product, 1)
    collection = Collection()
    collection.title = 'Coffee'
    collection.featured_product = Product(pk=1)
    collection.save()
    update = Product.objects.filter(pk=10).update(title="title")

    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 15
        item.save()

    context={
        'tags' : list(content),
        'update' : update,
    }
    return render(request, 'tags/tags.html', context)