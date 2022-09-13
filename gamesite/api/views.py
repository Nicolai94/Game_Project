from django.shortcuts import render
from rest_framework import viewsets, generics
from rest_framework import permissions

from api.serializers import NewsSerializer, GamesSerializer, CinemaSerializer, CommentNewsSerializer, \
 CommentCinemaSerializer, CommentGamesSerializer, ProductsSerializer, CommentProductsSerializer, CustomerSerializer, \
OrderSerializer
from main.models import News, Games, CinemaNews, Comment, CinemaComment, GamesComment, GamesCategory
from rest_framework.decorators import action
from rest_framework.response import Response
from shop.models import Product, ProductComment, Customer, Order


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]

    # put request
    # def put(self, request, *args, **kwargs):
    #     pk = kwargs.get('pk', None)
    #     if not pk:
    #         return Response({'error': 'Vethod Put not allowed'})
    #
    #     try:
    #         instance = News.objects.get(pk=pk)
    #     except:
    #         return Response({'error': 'Objects does not exists'})
    #     serializer = NewsSerializer(data=request.data, instance=instance)
    #     serializer.is_valid(raise_exception = True)
    #     serializer.save()
    #     return Response({'post': serializer.data})

    # def delete(self, request, *args, **kwargs):
    #     pk = kwargs.get('pk', None)
    #     if not pk:
    #         return Response({'error': 'Method DELETE not allowed'})
    #
    #     try:
    #         instance = News.objects.get(pk=pk)
    #     except:
    #         return Response({'error': 'Objects does not exists'})
    #     serializer = NewsSerializer(data=request.data, instance=instance)
    #     serializer.is_valid(raise_exception = True)
    #     serializer.delete()
    #     return Response({'post': serializer.data})



class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all().order_by('-id')
    serializer_class = GamesSerializer

    # def get_queryset(self):
    #     pk = self.kwargs.get('pk')
    #     if not pk:
    #         return Games.objects.all()[:3]
    #     return Games.objects.filter(pk=pk)

    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        cats = GamesCategory.objects.get(pk=pk)
        return Response({'cats': cats.name})
    #permission_classes = [permissions.IsAuthenticated]


class CinemaViewSet(viewsets.ModelViewSet):
    queryset = CinemaNews.objects.all().order_by('-id')
    serializer_class = CinemaSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentNewsViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-id')
    serializer_class = CommentNewsSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentCinemaViewSet(viewsets.ModelViewSet):
    queryset = CinemaComment.objects.all().order_by('-id')
    serializer_class = CommentCinemaSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentGamesViewSet(viewsets.ModelViewSet):
    queryset = GamesComment.objects.all().order_by('-id')
    serializer_class = CommentGamesSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductsSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentProductsViewSet(viewsets.ModelViewSet):
    queryset = ProductComment.objects.all().order_by('-id')
    serializer_class = CommentProductsSerializer
    permission_classes = [permissions.IsAuthenticated]


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-id')
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-id')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

