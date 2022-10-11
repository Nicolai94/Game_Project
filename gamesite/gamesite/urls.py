
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from api.views import NewsViewSet, GamesViewSet, CinemaViewSet, CommentNewsViewSet, CommentCinemaViewSet, CommentCinemaViewSet,\
CommentGamesViewSet, ProductsViewSet, CommentProductsViewSet, CustomerViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'news', NewsViewSet, basename='news')
router.register(r'games', GamesViewSet, basename='games')
router.register(r'cinema', CinemaViewSet, basename='cinema')
router.register(r'comment', CommentNewsViewSet, basename='comment_news')
router.register(r'comment-cinema', CommentCinemaViewSet, basename='Comment_cinema')
router.register(r'comment-games', CommentGamesViewSet, basename='Comment_games')
router.register(r'products', ProductsViewSet, basename='Products')
router.register(r'comment-products', CommentProductsViewSet, basename='Comment_products')
router.register(r'customer', CustomerViewSet, basename='customer')
router.register(r'order', OrderViewSet, basename='order')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('main.urls')),
    path('shop/', include('shop.urls')),
    path('forum/', include('forum.urls')),
    path('api/', include(router.urls)),
    # path('api/', include('api.urls')),
    path('api-auth/drf/', include('rest_framework.urls')),# systeme authentication here
    path(r'api-auth/', include('djoser.urls')),
    path(r'^auth/', include('djoser.urls.authtoken')),
    path('chat/', include('chat.urls')),
]
