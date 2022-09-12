from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from main.views import HomeView, NewsDetailView, ContactView, NewsView, CinemaNewsView, GamesView, \
    GamesDetailView, CinemaDetailView, AboutView, AddComment, AddCommentCinema, AddCommentGames, SearchView, \
    AdminNewsCreateView, AdminNewsListView, AdminGamesCreateView, AdminGamesListView, AdminCinemaCreateView, \
    AdminCinemaListView, AdminDeleteNewsView, AdminDeleteCinemaView, AdminDeleteGamesView, AdminCinemaUpdateView, \
    AdminNewsUpdateView, AdminGamesUpdateView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('news/', NewsView.as_view(), name='news'),
    path('news/<str:slug>/', NewsDetailView.as_view(), name='news_detail'),
    path('comment-news/<int:pk>/', AddComment.as_view(), name='comment_news'),
    path('games/', GamesView.as_view(), name='games'),
    path('games/<str:slug>/', GamesDetailView.as_view(), name='games_detail'),
    path('comment-games-news/<int:pk>/', AddCommentGames.as_view(), name='comment_games_news'),
    path('cinema/', CinemaNewsView.as_view(), name='cinema'),
    path('cinema/<str:slug>/', CinemaDetailView.as_view(), name='cinema_detail'),
    path('comment-cinema-news/<int:pk>/', AddCommentCinema.as_view(), name='comment_cinema_news'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about'),
    path('search/', SearchView.as_view(), name='search'),
    #adminpages
    path('admin-news/add/', AdminNewsCreateView.as_view(), name='adminnewscreate'),
    path('admin-news/list/', AdminNewsListView.as_view(), name='adminnewslist'),
    path('admin-games/add/', AdminGamesCreateView.as_view(), name='admingamescreate'),
    path('admin-games/list/', AdminGamesListView.as_view(), name='admingameslist'),
    path('admin-cinema/add/', AdminCinemaCreateView.as_view(), name='admincinemacreate'),
    path('admin-cinema/list/', AdminCinemaListView.as_view(), name='admincinemalist'),
    path('delete-news/<str:slug>/', AdminDeleteNewsView.as_view(), name='delete_news'),
    path('update-news/<str:slug>/', AdminNewsUpdateView.as_view(), name='update_news'),
    path('delete-cinema/<str:slug>/', AdminDeleteCinemaView.as_view(), name='delete_cinema'),
    path('update-cinema/<str:slug>/', AdminCinemaUpdateView.as_view(), name='update_cinema'),
    path('delete-games/<str:slug>/', AdminDeleteGamesView.as_view(), name='delete_games'),
    path('update-games/<str:slug>/', AdminGamesUpdateView.as_view(), name='update_games'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
