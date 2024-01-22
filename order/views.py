from rest_framework import generics, permissions
from .serializers import OrderSerializer
from rest_framework.response import Response
from .models import Order


class OrderAPIVIew(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = user.orders.all()
        serializer = OrderSerializer(instance=orders, many=True)
        return Response(serializer.data, status=200)


class OrderConfirmView(generics.RetrieveAPIView):
    def get(self, request, pk, *args, **kwargs):
        order = Order.objects.get(pk=pk)
        order.status = 'completed'
        order.save()
        return Response({'message': 'Вы подвердили заказ!'}, status=200)
