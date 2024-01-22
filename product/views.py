import logging

from django.core.cache import cache
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsAuthor
from rest_framework import permissions
from rating.serializers import RatingSerializer
from rest_framework.response import Response

logger = logging.getLogger(__name__)


@method_decorator(cache_page(60*10), name='dispatch')
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return (IsAuthor(),)
        return (permissions.IsAuthenticatedOrReadOnly(),)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        cache.clear()

    def perform_destroy(self, instance):
        instance.delete()
        cache.clear()

    @action(['GET', 'POST', 'DELETE'], detail=True)
    def ratings(self, request, pk):
        product = self.get_object()
        user = request.user

        if request.method == 'GET':
            rating = product.ratings.all()
            serializer = RatingSerializer(instance=rating, many=True)
            logger.info(f"GET request for ratings of product {pk} by user {user}")
            return Response(serializer.data, status=200)

        elif request.method == 'POST':
            if product.ratings.filter(owner=user).exists():
                logger.warning(f"User {user} attempted to post a rating on product {pk} more than once")
                return Response('Ты уже поставил рейтинг на этот товар', status=400)
            serializer = RatingSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(owner=user, product=product)
            logger.info(f"POST request to add a rating on product {pk} by user {user}")
            return Response(serializer.data, status=201)

        else:
            if not product.ratings.filter(owner=user).exists():
                logger.warning(f"User {user} attempted to delete a rating on product {pk} without leaving a review")
                return Response('Ты не можешь удалить, потому что ты не оставлял отзыв', status=400)
            rating = product.ratings.get(owner=user)
            rating.delete()
            logger.info(f"DELETE request to remove a rating on product {pk} by user {user}")
            return Response('Успешно удалено', status=204)

