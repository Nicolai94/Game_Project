from django.urls import path

from forum.views import HomeForumView

urlpatterns = [
    path('', HomeForumView.as_view(), name='forum_home'),
    ]