from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import *
from django.contrib.postgres.search import SearchVector
from main.models import News, CinemaNews, Games, NewsImage, GamesImage, CinemaImage
from shop.models import Product, Admin
from main.forms import CommentForm, CinemaCommentForm, GamesCommentForm, NewsForm, GamesForm, CinemaForm


class HomeView(TemplateView):
    template_name = 'main/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_news = News.objects.all().order_by('-id')[:4]
        all_games = Games.objects.all().order_by('-id')[:4]
        all_products = Product.objects.all().order_by('-id')[:4]
        context['all_games'] = all_games
        context['all_news'] = all_news
        context['all_products'] = all_products
        return context


class NewsDetailView(DetailView):
    model = News
    template_name = 'main/news_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        url_slug = self.kwargs['slug']
        news = News.objects.get(slug=url_slug)
        news.save()
        context['news'] = news
        return context


class AddComment(View):

    def post(self, request, pk):
        form = CommentForm(request.POST)
        news = News.objects.get(id=pk)
        if form.is_valid():
            ''' Stop save form'''
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.news = news
            form.save()
        return redirect(news.get_absolute_url())


class AddCommentCinema(View):

    def post(self, request, pk):
        form = CinemaCommentForm(request.POST)
        cinema_news = CinemaNews.objects.get(id=pk)
        if form.is_valid():
            ''' Stop save form'''
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.cinema = cinema_news
            form.save()
        return redirect(cinema_news.get_absolute_url())


class AddCommentGames(View):

    def post(self, request, pk):
        form = GamesCommentForm(request.POST)
        games_news = Games.objects.get(id=pk)
        if form.is_valid():
            ''' Stop save form'''
            form = form.save(commit=False)
            if request.POST.get('parent', None):
                form.parent_id = int(request.POST.get('parent'))
            form.games = games_news
            form.save()
        return redirect(games_news.get_absolute_url())


class ContactView(TemplateView):
    template_name = 'main/contact.html'


class AboutView(TemplateView):
    template_name = 'main/about.html'


class NewsView(ListView):
    model = News
    template_name = 'main/news_list.html'
    context_object_name = 'news'
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'News page'
        return context

    def get_queryset(self):
        return News.objects.filter(available=True).order_by('-created')


class CinemaNewsView(ListView):
    model = CinemaNews
    template_name = 'main/cinema_list.html'
    context_object_name = 'cinema_news'
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Cinema news page'
        return context

    def get_queryset(self):
        return CinemaNews.objects.filter(available=True).order_by('-created')


class CinemaDetailView(DetailView):
    model = CinemaNews
    template_name = 'main/cinema_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        url_slug = self.kwargs['slug']
        cinema = CinemaNews.objects.get(slug=url_slug)
        cinema.save()
        context['cinema'] = cinema
        return context


class GamesView(ListView):
    model = Games
    template_name = 'main/games_list.html'
    context_object_name = 'games'
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Games page'
        all_products = Product.objects.all().order_by('-id')[:4]
        context['all_products'] = all_products
        return context

    def get_queryset(self):
        return Games.objects.filter(available=True).order_by('-created')


class GamesDetailView(DetailView):
    model = Games
    template_name = 'main/games_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        url_slug = self.kwargs['slug']
        game = Games.objects.get(slug=url_slug)
        game.save()
        context['game'] = game
        return context


class SearchView(TemplateView):
    template_name = 'main/search.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        kw = self.request.GET.get('keyword')
        results = News.objects.annotate(search=SearchVector('title', 'content'), ).filter(search=kw)
        context['results'] = results
        return context


# Admin Pages

class AdminRequiredMixin(object):

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        if request.user.is_authenticated and Admin.objects.filter(user=request.user).exists():
            pass
        else:
            return redirect('/admin-login/')
        return super().dispatch(request, *args, **kwargs)


class AdminNewsCreateView(AdminRequiredMixin, CreateView):
    template_name = 'adminpages/adminnewscreate.html'
    form_class = NewsForm
    success_url = reverse_lazy('adminnewslist')

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist('more_images')
        for i in images:
            NewsImage.objects.create(news=p, image=i)
        return super().form_valid(form)


class AdminNewsListView(ListView):
    template_name = 'adminpages/adminnewslist.html'
    queryset = News.objects.all().order_by('-id')
    context_object_name = 'allnews'


class AdminDeleteNewsView(DeleteView):
    model = News
    template_name = 'adminpages/admin_confirm_delete.html'
    success_url = reverse_lazy('adminnewslist')


class AdminNewsUpdateView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = 'adminpages/admin_update_form.html'
    success_url = '/admin-news/list/'


class AdminGamesCreateView(AdminRequiredMixin, CreateView):
    template_name = 'adminpages/admingamescreate.html'
    form_class = GamesForm
    success_url = reverse_lazy('admingameslist')

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist('more_images')
        for i in images:
            GamesImage.objects.create(product=p, image=i)
        return super().form_valid(form)


class AdminGamesListView(ListView):
    template_name = 'adminpages/admingameslist.html'
    queryset = Games.objects.all().order_by('id')
    context_object_name = 'allgames'


class AdminDeleteGamesView(DeleteView):
    model = Games
    template_name = 'adminpages/admin_confirm_delete.html'
    success_url = reverse_lazy('admingameslist')


class AdminGamesUpdateView(UpdateView):
    model = Games
    form_class = GamesForm
    template_name = 'adminpages/admin_update_form.html'
    success_url = '/admin-games/list/'


class AdminCinemaCreateView(AdminRequiredMixin, CreateView):
    template_name = 'adminpages/admincinemacreate.html'
    form_class = CinemaForm
    success_url = reverse_lazy('admincinemalist')

    def form_valid(self, form):
        p = form.save()
        images = self.request.FILES.getlist('more_images')
        for i in images:
            CinemaImage.objects.create(product=p, image=i)
        return super().form_valid(form)


class AdminCinemaListView(ListView):
    template_name = 'adminpages/admincinemalist.html'
    queryset = CinemaNews.objects.all().order_by('id')
    context_object_name = 'allcinema'


class AdminDeleteCinemaView(DeleteView):
    model = CinemaNews
    template_name = 'adminpages/admin_confirm_delete.html'
    success_url = reverse_lazy('admincinemalist')


class AdminCinemaUpdateView(UpdateView):
    model = CinemaNews
    form_class = CinemaForm
    template_name = 'adminpages/admin_update_form.html'
    success_url = '/admin-cinema/list/'
