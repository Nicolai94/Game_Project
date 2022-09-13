from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from api.serializers import NewsSerializer, GamesSerializer, CinemaSerializer, CommentNewsSerializer, \
 CommentCinemaSerializer, CommentGamesSerializer, ProductsSerializer, CommentProductsSerializer, CustomerSerializer, \
OrderSerializer
from main.models import News, Games, CinemaNews, Comment, CinemaComment, GamesComment
from shop.models import Product, ProductComment, Customer, Order


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]



class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all().order_by('-id')
    serializer_class = GamesSerializer
    permission_classes = [permissions.IsAuthenticated]


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

