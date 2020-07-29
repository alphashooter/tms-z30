from shop.models import *
from rest_framework.serializers import *
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.mixins import *
from rest_framework.permissions import IsAuthenticated


__all__ = 'ProductSerializer', 'ProductViewSet'


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class ProductViewSet(ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ProductSerializer


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class OrderViewSet(ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user: User = self.request.user
        order = Order.objects.get_or_create(user=user, name='x', tel='x', address='x')[0]
        return order,


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'amount', 'item']


class OrderItemViewSet(ModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user: User = self.request.user
        order = Order.objects.get_or_create(user=user, name='x', tel='x', address='x')[0]
        return OrderItem.objects.filter(order=order)


router = DefaultRouter()
router.register('products', ProductViewSet, 'product')
router.register('orders', OrderViewSet, 'order')
router.register('cart', OrderItemViewSet, 'cart')
