from django.urls import path
from rest_framework_nested import routers
from pprint import pprint
from .views import ProductViewSet, CollectionViewSet, ReviewViewSet, CartViewSet, CartItemViewSet, \
      CustomerViewSet, OrderViewSet


router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='product')
router.register('collections', CollectionViewSet)
router.register('carts', CartViewSet)
router.register('customers', CustomerViewSet)
router.register('orders', OrderViewSet, basename='orders')

product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('reviews', ReviewViewSet, basename='product-reviews')
# pprint(router.urls)

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + product_router.urls + carts_router.urls