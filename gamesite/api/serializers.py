from rest_framework import serializers, generics

from main.models import News, Games, CinemaNews, Comment, CinemaComment, GamesComment, GamesCategory
from shop.models import Product, ProductComment, Customer, Order


class NewsSerializer(serializers.HyperlinkedModelSerializer):
    category_name = serializers.CharField(source='category.name')

    class Meta:
        model = News
        fields = ['title', 'slug',  'created', 'updated', 'category_name']


class GamesSerializer(serializers.HyperlinkedModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Games
        fields = ['title', 'slug', 'content', 'created', 'available', 'category_name']

    def create(self, validated_data):
        category = []
        if 'category' in validated_data:
            category = validated_data.pop('category')
        games = Games.objects.create(**validated_data)
        print(games)

        for cat in category:
            GamesCategory.objects.create(games=games, **cat)
        return games


class CinemaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CinemaNews
        fields = ['title', 'slug', 'content', 'created', 'available']


class CommentNewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'content', 'created', 'active']


class CommentCinemaSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CinemaComment
        fields = ['name', 'email', 'content', 'created', 'active']


class CommentGamesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = GamesComment
        fields = ['name', 'email', 'content', 'created', 'active']


class ProductsSerializer(serializers.HyperlinkedModelSerializer):
    category_title = serializers.CharField(source='category.title')

    class Meta:
        model = Product
        fields = ['title', 'slug', 'price', 'description', 'minimal_requirements', 'normal_requirements', 'view_count', 'category_title']


class CommentProductsSerializer(serializers.HyperlinkedModelSerializer):
    products = serializers.CharField(source='products.title')

    class Meta:
        model = ProductComment
        fields = ['name', 'email', 'content', 'created', 'active', 'products']


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Customer
        fields = ['full_name', 'address',  'joined_on']


class OrderSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Order
        fields = ['ordered_by', 'shipping_address', 'mobile', 'email', 'total', 'order_status', 'created_at']

