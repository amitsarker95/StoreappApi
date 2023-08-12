from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser, DjangoModelPermissions
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin, CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status

from .models import Product, Collection, OrderItem, Review, Cart, CartItem, Customer, Order

from .serializers import ProductSerializers, CollectionSerializers, ReviewSerializers, \
CartSerializers, CartItemSerializers, AddCartItemSerializers, UpdateCartItemSerializers, CustomerSerializers, \
OrderSerializers, CreateOrderSerializers

from .filters import ProductFilter
from .pagination import DefaultPagination
from .permissions import IsOwnerOrReadOnly , IsStaffOrReadOnly, ViewCustomerHistoryPermission


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    permission_classes = [IsStaffOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'inventory']

    def get_serializer_context(self):
        return {'request' : self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product can not be deleted.'},status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)
    
        

class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('product')).all()
    serializer_class = CollectionSerializers
    permission_classes = [IsStaffOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id = kwargs['pk']).count() > 0:
            return Response({'error' : 'This collection can not be deleted.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)



class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id' : self.kwargs['product_pk']}
    

class CartViewSet(
        CreateModelMixin,
        RetrieveModelMixin,
        GenericViewSet,
        DestroyModelMixin):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializers

class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializers
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializers
        return CartItemSerializers
    
    def get_serializer_context(self):
        return {'cart_id' : self.kwargs['cart_pk']}

    def get_queryset(self):
        item = CartItem.objects\
            .filter(cart_id = self.kwargs['cart_pk'])\
            .select_related('product')
        return item
#Testing git push


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializers
    permission_classes = [DjangoModelPermissions]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes = [IsAuthenticated])
    def me(self, request):
        (customer, created) = Customer.objects.get_or_create(user_id = request.user.id)
        if request.method == "GET":
            serializer = CustomerSerializers(customer)
            return Response(serializer.data)
        if request.method == "PUT":
            serializer = CustomerSerializers(customer, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        

class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializers(
            data=request.data,
            context = {'user_id' : self.request.user.id}
            )
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializers(order)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializers
        return OrderSerializers
    
    def get_serializer_context(self):
        return {'user_id' : self.request.user.id}

    def get_queryset(self):
        user = self.request.user
        (customer_id, created) = Customer.objects.only('id').get_or_create(user_id=user.id)
        if user.is_staff:
            return Order.objects.all()
        return Order.objects.filter(customer_id=customer_id)


