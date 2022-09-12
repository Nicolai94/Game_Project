from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from embed_video.fields import EmbedVideoField


class CategoryNews(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, null=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category News'
        verbose_name_plural = 'Categories News'


class News(models.Model):
    title = models.CharField(max_length=250, verbose_name='News')
    slug = models.SlugField(max_length=200, db_index=True, null=True, unique=True)
    content = models.TextField(blank=True, verbose_name='Description')
    image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Published')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated')
    available = models.BooleanField(default=True)
    category = models.ForeignKey(CategoryNews, on_delete=models.PROTECT, related_name='news',
                                 verbose_name='Category')

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_detail', kwargs={'slug': self.slug})

    def get_comment(self):
        return self.comment_set.filter(parent__isnull=True)


class NewsImage(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/images/', blank=True)

    def __str__(self):
        return self.news.title


class Comment(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    news = models.ForeignKey(News, on_delete=models.CASCADE, verbose_name='news')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='parent')

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.news)

    class Meta:
        ordering = ('created',)


class CinemaNews(models.Model):
    title = models.CharField(max_length=250, verbose_name='Cinema_News')
    slug = models.SlugField(max_length=200, db_index=True, null=True, unique=True)
    content = models.TextField(blank=True, verbose_name='Description')
    image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='Published')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated')
    available = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cinema News'
        verbose_name_plural = 'Cinema News'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('cinema_detail', kwargs={'slug': self.slug})

    def get_comment(self):
        return self.comment_set.filter(parent__isnull=True)


class CinemaImage(models.Model):
    cinema_news = models.ForeignKey(CinemaNews, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/images/', blank=True)

    def __str__(self):
        return self.cinema_news.title


class CinemaComment(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    cinema = models.ForeignKey(CinemaNews, on_delete=models.CASCADE, verbose_name='news')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='parent')

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.cinema)

    class Meta:
        ordering = ('created',)


class GamesCategory(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, null=True, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('games', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('name',)
        verbose_name = 'Games Category'
        verbose_name_plural = 'Games Categories'


class Games(models.Model):
    title = models.CharField(max_length=250, verbose_name='Games')
    slug = models.SlugField(max_length=200, db_index=True, null=True, unique=True)
    content = models.TextField(blank=True, verbose_name='Description')
    image = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    video = EmbedVideoField(null=True, blank=True, verbose_name='Video')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Published')
    updated = models.DateTimeField(auto_now=True, verbose_name='Updated')
    available = models.BooleanField(default=True)
    category = models.ForeignKey(GamesCategory, on_delete=models.PROTECT, related_name='games', null=True, blank=True,
                                 verbose_name='Game Category')

    class Meta:
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
        ordering = ('-created',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('games_detail', kwargs={'slug': self.slug})


class GamesImage(models.Model):
    games_news = models.ForeignKey(Games, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/%Y/%m/%d/images/', blank=True)

    def __str__(self):
        return self.games_news.title


class GamesComment(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    games = models.ForeignKey(Games, on_delete=models.CASCADE, verbose_name='games_news')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, verbose_name='parent')

    def __str__(self):
        return 'Comment by {} on {}'.format(self.name, self.games)

    class Meta:
        ordering = ('created',)

