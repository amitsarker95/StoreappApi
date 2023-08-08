from django.shortcuts import render
from django.http import HttpResponse
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, F, Func, Value, DecimalField
from django.db.models.expressions import ExpressionWrapper
from django.db.models.aggregates import Count, Min, Max, Sum
from django.db.models.functions import Concat
from store.models import Product, OrderItem, Order, Customer

# Create your views here.

def say_hello(request):
    # query_set = Product.objects.all()
    # for product in query_set:
    #     print(product)
    # try:
    #     product = Product.objects.get(pk=1)
    # except ObjectDoesNotExist:
    #     pass

    # product = Product.objects.filter(unit_price__range=(20, 30))
    # product = Product.objects.filter(inventory__lt=20).filter(unit_price__lt=20)
    # product = Product.objects.filter(Q(inventory__lt=20) | Q(unit_price__lt=30))
    # queryset = Product.objects.filter(inventory = F("unit_price"))
    # return boolean
    # exists = Product.objects.filter(pk=1).exists()
    # sorteddata = Product.objects.order_by('title')
    # sorteddata = Product.objects.order_by('unit_price','-title').reverse()
    # firstdata = Product.objects.order_by('title')[0]
    # first = Product.objects.earliest('title')
    # last = Product.objects.latest('title')
    # limitdata = Product.objects.all()[:5]
    # spacific = Product.objects.values('title', 'description', 'collection__title')
    # spacificlist = Product.objects.values_list('title', 'description', 'collection__title')
    # ordered = OrderItem.objects.values('product_id')
    # ordered_product = Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')
    # ordered = OrderItem.objects.values('product_id').distinct()
    # product = Product.objects.only('title', 'description')
    # product = Product.objects.defer('description')
    # product = Product.objects.select_related('collection').all()
    # queryset = Product.objects.filter(inventory = F("collection__id"))
    # product = Product.objects.filter(Q(inventory__lt=20) & ~Q(unit_price__lt=30))
    # productX = Product.objects.select_related('collection').all()
    # productY = Product.objects.prefetch_related('promotions').select_related('collection').all()
    # orders = Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    # total_product = Product.objects.filter(collection__id=1).aggregate(count=Count('id'), min_price=Min('unit_price'))
    # customer = Customer.objects.annotate(new_id=F('id') + 2)[:5]
    # concat = Customer.objects.annotate(
    #     full_name = Func(F('first_name'), Value(' '),
    #                      F('last_name'), function='CONCAT')
    # )
    # concat_two = Customer.objects.annotate(
    #     full_name = Concat('first_name', Value(' '), 'last_name')
    # )
    # per_customer_total_order = Customer.objects.annotate(
    #     total_order = Count('order')
    # )
    # discount_price = ExpressionWrapper(F('unit_price') * 8, output_field=DecimalField())
    # discount = Product.objects.annotate(
    #     discount_price = discount_price
    # )
    # context = {
    #     'products' : list(product),
    #     'productX' : list(productX),
    #     'productY' : list(productY),
    #     'querys': list(queryset),
    #     'sortdata' : sorteddata,
    #     'firstdata' : firstdata,
    #     'first' : first,
    #     'last' : last,
    #     'limitdata' : list(limitdata),
    #     'spacific' : list(spacific),
    #     'spacificlist' : list(spacificlist),
    #     'ordered' : list(ordered),
    #     'ordered_product' : list(ordered_product),
    #     'orders' : list(orders),
    #     'total_product': total_product,
    #     'customer' : list(customer),
    #     'discount' : discount,
        
        
    # }

    url = 'http://127.0.0.1:8000/auth/users/me/'

    # Set the JWT token
    jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNjkxNjAxMDk1LCJpYXQiOjE2OTE1MTQ2OTUsImp0aSI6ImRiNTA3OTBjOGI1ZTRhYzk5NDllYmJmNzFhMzU2YWJlIiwidXNlcl9pZCI6Nn0.-Y_QMVB8cd-kGHtdxe63Wmf-5jaHV9q-jZB35Xd3UC4'

    # Set the headers with the Authorization header containing the JWT token
    headers = {
        'Authorization': f'JWT {jwt_token}'
    }

    # Create a dictionary of data for the POST request (if needed)
    data = {
        'key': 'value'
    }

    # Send the POST request
    response = requests.post(url, headers=headers, data=data)

    # Check the response
    if response.status_code == 200:
        print('Request was successful!')
        print('Response:', response.json())
    else:
        print('Request failed.')
        print('Response:', response.text)

    
    return HttpResponse("Okay")




