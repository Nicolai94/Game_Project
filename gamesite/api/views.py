from django.shortcuts import render
from rest_framework import viewsets, generics, status
from rest_framework import permissions

from api.serializers import NewsSerializer, GamesSerializer, CinemaSerializer, CommentNewsSerializer, \
 CommentCinemaSerializer, CommentGamesSerializer, ProductsSerializer, CommentProductsSerializer, CustomerSerializer, \
OrderSerializer
from main.models import News, Games, CinemaNews, Comment, CinemaComment, GamesComment, GamesCategory
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import action
from rest_framework.generics import *
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from shop.models import Product, ProductComment, Customer, Order
from .permissions import IsAdminOrReadOnly


# class NewsView(APIView):
#
#     def get(self, request):
#         news = News.objects.all()
#         serializer = NewsSerializer(news, many=True)
#         return Response(serializer.data)
#
#     def post(self, request):
#         serializer = NewsSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all().order_by('-id')
    serializer_class = NewsSerializer
    permission_classes = [permissions.IsAuthenticated]


class GamesAPIListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 2


class GamesViewSet(viewsets.ModelViewSet):
    queryset = Games.objects.all().order_by('-id')
    serializer_class = GamesSerializer
    permission_classes = [IsAdminOrReadOnly] #custom class
    authentication_classes = [TokenAuthentication]
    pagination_class = GamesAPIListPagination

    @action(methods=['get'], detail=True)
    def category(self, request, pk=None):
        cats = GamesCategory.objects.get(pk=pk)
        return Response({'cats': cats.name}, status=status.HTTP_202_ACCEPTED)



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

