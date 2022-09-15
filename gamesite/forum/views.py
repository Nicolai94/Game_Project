from django.shortcuts import render
from django.views.generic import TemplateView


class HomeForumView(TemplateView):
    template_name = 'forum/forum_base.html'
